import joblib
import pandas as pd

# Load model saat pertama kali
mlp_model = joblib.load('model_mlp.pkl')
svm_model = joblib.load('model_svm.pkl')

def predict_disease(usia, jenis_kelamin, gejala_list, algoritma="MLP"):
    # Persiapkan data input untuk prediksi
    input_data = {
        'Usia': usia,
        'Jenis Kelamin': 1 if jenis_kelamin == 'Perempuan' else 0,  # Mengonversi jenis kelamin ke angka
        'Gejala': ', '.join(gejala_list)
    }

    # Jika ada fitur 'Keluhan_Feat', tambahkan kolom ini
    # Misalnya, kita asumsikan 'Keluhan_Feat' dihitung dari jumlah gejala atau dengan cara lain
    input_data['Keluhan_Feat'] = len(gejala_list)  # Menambahkan jumlah gejala sebagai fitur 'Keluhan_Feat'

    # Memastikan data dalam format yang benar (bisa berupa DataFrame atau array tergantung model)
    df = pd.DataFrame([input_data])

    # Cek apakah kolom yang diperlukan ada di dalam DataFrame
    required_columns = ['Usia', 'Jenis Kelamin', 'Gejala', 'Keluhan_Feat']
    for col in required_columns:
        if col not in df.columns:
            df[col] = 0  # Jika kolom hilang, beri nilai default (misalnya 0)

    # Menggunakan model yang dipilih untuk prediksi
    if algoritma == "MLP":
        prediksi = mlp_model.predict(df[['Usia', 'Jenis Kelamin', 'Gejala', 'Keluhan_Feat']])[0]
    elif algoritma == "SVM":
        prediksi = svm_model.predict(df[['Usia', 'Jenis Kelamin', 'Gejala', 'Keluhan_Feat']])[0]
    else:
        prediksi = "Model tidak ditemukan"

    return prediksi
