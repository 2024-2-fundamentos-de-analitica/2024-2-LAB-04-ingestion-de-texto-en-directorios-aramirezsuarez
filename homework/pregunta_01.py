from pathlib import Path
import shutil
import pandas as pd
from glob import glob
import fileinput
import zipfile

def _create_output_directory(output_directory):
    output_path = Path(output_directory)
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True, exist_ok=True)

def _save_output(output_directory, filename, df):
    output_path = Path("files") / output_directory
    output_path.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path / f"{filename}.csv", index=False)

def pregunta_01():
    zip_path = Path("files/input.zip")
    input_dir = Path("files/input")

    # Asegurarse de que el directorio de entrada esté vacío
    _create_output_directory(input_dir)

    # Extraer archivos directamente en `files/input` sin crear subcarpetas
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            zip_ref.extract(file, input_dir)
    
    # Cargar y procesar datos
    seq = []
    files = glob(f"{input_dir}/**/*.txt", recursive=True)
    with fileinput.input(files=files) as f:
        for line in f:
            seq.append((f.filename(), line.strip()))

    train_data, test_data = [], []
    for k, v in seq:
        target = (
            "neutral"
            if "neutral" in k
            else "negative" if "negative" in k else "positive"
        )
        data = {"phrase": v, "target": target}
        if "train" in k:
            train_data.append(data)
        else:
            test_data.append(data)

    train_dataset = pd.DataFrame(train_data)
    test_dataset = pd.DataFrame(test_data)

    # Crear directorio de salida y guardar los datasets
    _create_output_directory("files/output")
    _save_output("output", "train_dataset", train_dataset)
    _save_output("output", "test_dataset", test_dataset)

    return 1

pregunta_01()
