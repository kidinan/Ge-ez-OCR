import torch
import torch.nn as nn
import torchvision.transforms as transforms

# Define the character to index mapping
geez_char = ' ኊሀሁሂሃሄህሆሇለሉሊላሌልሎሏሐሑሒሓሔሕሖሗመሙሚማሜምሞሟሠሡሢሣሤሥሦሧረሩሪራሬርሮሯሰሱሲሳሴስሶሷሸሹሺሻሼሽሾሿቀቁቂቃቄቅቆቇቐቑቒቓቔቕቖቘቚቛቜቝበቡቢባቤብቦቧቨቩቪቫቬቭቮቯተቱቲታቴትቶቷቸቹቺቻቼችቾቿኀኁኂኃኋኄኅኌኆኇነኑኒናኔንኖኗኘኙኚኛኜኝኞኟአኡኢኣኤእኦኧከኩኪካኬክኮኯኰኲኳኴኵኸኹኺኻኼኽኾዀዂዃዄዅወዉዊዋዌውዎዏዐዑዒዓዔዕዖዘዙዚዛዜዝዞዟዠዡዢዣዤዥዦዧየዩዪያዬይዮዯደዱዲዳዴድዶዷዸዹዺዻዼዽዾዿጀጁጂጃጄጅጆጇገጉጊጋጌግጎጏጐጒጓጔጕጘጙጚጛጜጝጞጟጠጡጢጣጤጥጦጧጨጩጪጫጬጭጮጯጰጱጲጳጴጵጶጷጸጹጺጻጼጽጾጿፀፁፂፃፄፅፆፇፈፉፊፋፌፍፎፏፐፑፒፓፔፕፖፗ፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፼፻ቈቊኍኈቍቌ:ቋ«፠፡።፣፥፦፧፨()[]፤»-'
char_to_idx = {char: idx + 1 for idx, char in enumerate(geez_char)}
char_to_idx['<PAD>'] = 0
idx_to_char = {idx: char for char, idx in char_to_idx.items()}

class OCRModel(nn.Module):
    def __init__(self, num_classes, rnn_size=128):
        super(OCRModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 64, kernel_size=3, padding=1)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool2 = nn.MaxPool2d(kernel_size=(2, 1))
        self.conv3 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.conv4 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.pool3 = nn.MaxPool2d(kernel_size=(2, 1))
        self.conv5 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.batch_norm1 = nn.BatchNorm2d(512)
        self.conv6 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.batch_norm2 = nn.BatchNorm2d(512)
        self.pool4 = nn.MaxPool2d(kernel_size=(2, 1))
        self.conv7 = nn.Conv2d(512, 512, kernel_size=2)
        self.blstm1 = nn.LSTM(512, rnn_size, bidirectional=True, batch_first=True)
        self.blstm2 = nn.LSTM(rnn_size*2, rnn_size, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(rnn_size*2, num_classes + 1)

    def forward(self, x):
        x = self.pool1(torch.relu(self.conv1(x)))
        x = self.pool2(torch.relu(self.conv2(x)))
        x = torch.relu(self.conv3(x))
        x = torch.relu(self.conv4(x))
        x = self.pool3(x)
        x = torch.relu(self.conv5(x))
        x = self.batch_norm1(x)
        x = torch.relu(self.conv6(x))
        x = self.batch_norm2(x)
        x = self.pool4(x)
        x = torch.relu(self.conv7(x))
        x = x.squeeze(2).permute(0, 2, 1)
        x, _ = self.blstm1(x)
        x, _ = self.blstm2(x)
        x = self.fc(x)
        return x

def load_ocr_model(model_path, num_classes):
    # Load OCR model
    ocr_model = OCRModel(num_classes=num_classes)
    ocr_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    ocr_model.eval()
    return ocr_model

# Define transforms for preprocessing the input image
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((32, 128)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# Decode predictions to readable text
def decode_predictions(preds, idx_to_char):
    preds = preds.argmax(2)  # Get the index of the max log-probability
    pred_strings = []
    for pred in preds:
        pred_string = ''.join([idx_to_char[idx.item()] for idx in pred if idx.item() != 0])
        pred_strings.append(pred_string)
    return pred_strings
