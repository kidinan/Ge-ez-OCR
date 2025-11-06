
import sys
sys.path.insert(0, '/opt/render/project/src')
import nest_asyncio
nest_asyncio.apply()

import logging
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import PlainTextResponse
from PIL import Image
from io import BytesIO
from app.services.yolo_service import load_yolo_model, detect_lines
from app.services.ocr_service import load_ocr_model, get_image_transform, process_ocr

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

# Define the character to index mapping
geez_char = ' ኊሀሁሂሃሄህሆሇለሉሊላሌልሎሏሐሑሒሓሔሕሖሗመሙሚማሜምሞሟሠሡሢሣሤሥሦሧረሩሪራሬርሮሯሰሱሲሳሴስሶሷሸሹሺሻሼሽሾሿቀቁቂቃቄቅቆቇቐቑቒቓቔቕቖቘቚቛቜቝበቡቢባቤብቦቧቨቩቪቫቬቭቮቯተቱቲታቴትቶቷቸቹቺቻቼችቾቿኀኁኂኃኋኄኅኌኆኇነኑኒናኔንኖኗኘኙኚኛኜኝኞኟአኡኢኣኤእኦኧከኩኪካኬክኮኯኰኲኳኴኵኸኹኺኻኼኽኾዀዂዃዄዅወዉዊዋዌውዎዏዐዑዒዓዔዕዖዘዙዚዛዜዝዞዟዠዡዢዣዤዥዦዧየዩዪያዬይዮዯደዱዲዳዴድዶዷዸዹዺዻዼዽዾዿጀጁጂጃጄጅጆጇገጉጊጋጌግጎጏጐጒጓጔጕጘጙጚጛጜጝጞጟጠጡጢጣጤጥጦጧጨጩጪጫጬጭጮጯጰጱጲጳጴጵጶጷጸጹጺጻጼጽጾጿፀፁፂፃፄፅፆፇፈፉፊፋፌፍፎፏፐፑፒፓፔፕፖፗ፩፪፫፬፭፮፯፰፱፲፳፴፵፶፷፸፹፺፼፻ቈቊኍኈቍቌ:ቋ«፠፡።፣፥፦፧፨()[]፤»-'
char_to_idx = {char: idx + 1 for idx, char in enumerate(geez_char)}
char_to_idx['<PAD>'] = 0
idx_to_char = {idx: char for char, idx in char_to_idx.items()}

# Load models
yolo_model = load_yolo_model('app/models/yolov5/best.pt')
ocr_model = load_ocr_model('app/models/ocr_model.pth', num_classes=len(geez_char))
transform = get_image_transform()

# Initialize FastAPI app
app = FastAPI()

@app.post("/predict", response_class=PlainTextResponse)
async def predict(file: UploadFile = File(...)):
    try:
        logger.info("Request received for /predict")
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert('RGB')
        
        # Detect lines using YOLOv5
        boxes = detect_lines(yolo_model, image)
        
        # Crop lines and process with OCR model
        lines = [image.crop((int(box[0]), int(box[1]), int(box[2]), int(box[3]))) for box in boxes]
        texts = []
        positions = []
        with torch.no_grad():
            for box, line_image in zip(boxes, lines):
                line_image_tensor = transform(line_image).unsqueeze(0)
                pred_texts = process_ocr(ocr_model, line_image_tensor, idx_to_char)
                texts.append(pred_texts[0])
                positions.append(f"{int(box[0])},{int(box[1])},{int(box[2])},{int(box[3])}")

        response_text = '\n'.join([f"{text}|{position}" for text, position in zip(texts, positions)])
        logger.info(f"Response: {response_text}")
        return response_text
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop="asyncio")
