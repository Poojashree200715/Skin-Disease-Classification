import evaluation as ev

model = ev.load_trained_model()
print("Model loaded successfully!")
model.summary()