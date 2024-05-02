import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from tkinter import *
import tkinter.font as font

# Load data
data = pd.read_csv('Placement.csv')

# Drop unnecessary columns
data = data.drop(['sl_no', 'salary'], axis=1)

# Map categorical variables to numerical values
data['ssc_b'] = data['ssc_b'].map({'Central': 1, 'Others': 0})
data['hsc_b'] = data['hsc_b'].map({'Central': 1, 'Others': 0})
data['hsc_s'] = data['hsc_s'].map({'Science': 2, 'Commerce': 1, 'Arts': 0})
data['degree_t'] = data['degree_t'].map({'Sci&Tech': 2, 'Comm&Mgmt': 1, 'Others': 0})
data['specialisation'] = data['specialisation'].map({'Mkt&HR': 1, 'Mkt&Fin': 0})
data['workex'] = data['workex'].map({'Yes': 1, 'No': 0})
data['status'] = data['status'].map({'Placed': 1, 'Not Placed': 0})

# Separate features and target variable
X = data.drop('status', axis=1)
y = data['status']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

# Define TensorFlow model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=0)

# Make predictions
y_pred = (model.predict(X_test) > 0.5).astype("int32")

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Save the trained model
model.save('model_campus_placement_tf')

# Load the trained model
model = tf.keras.models.load_model('model_campus_placement_tf')

# Tkinter GUI
def show_entry_fields():
    p1 = 1 if clicked.get() == "Male" else 0
    p2 = float(e2.get())
    p3 = 1 if clicked1.get() == "Central" else 0
    p4 = float(e4.get())
    p5 = 1 if clicked6.get() == "Central" else 0
    p6 = 2 if clicked2.get() == "Science" else (1 if clicked2.get() == "Commerce" else 0)
    p7 = float(e7.get())
    p8 = 2 if clicked3.get() == "Sci&Tech" else (1 if clicked3.get() == "Comm&Mgmt" else 0)
    p9 = 1 if clicked4.get() == "Yes" else 0
    p10 = float(e10.get())
    p11 = 1 if clicked5.get() == "Mkt&HR" else 0
    p12 = float(e12.get())

    new_data = pd.DataFrame({
        'gender': [p1],
        'ssc_p': [p2],
        'ssc_b': [p3],
        'hsc_p': [p4],
        'hsc_b': [p5],
        'hsc_s': [p6],
        'degree_p': [p7],
        'degree_t': [p8],
        'workex': [p9],
        'etest_p': [p10],
        'specialisation': [p11],
        'mba_p': [p12]
    })

    result = (model.predict(new_data) > 0.5).astype("int32")

    if result[0] == 0:
        Label(master, text="Not Placed").grid(row=31)
    else:
        Label(master, text="Student Will be Placed", font=("Arial", 15)).grid(row=31)


master = Tk()
master.title("Campus Placement Prediction System")

label = Label(master, text="Campus Placement Prediction System", bg="green", fg="white", font=("Arial", 20))
label.grid(row=0, columnspan=2)

Label(master, text="Gender", font=("Arial", 15)).grid(row=1)
Label(master, text="Secondary Education percentage- 10th Grade", font=("Arial", 15)).grid(row=2)
Label(master, text="Board of Education", font=("Arial", 15)).grid(row=3)
Label(master, text="Higher Secondary Education percentage- 12th Grade", font=("Arial", 15)).grid(row=4)
Label(master, text="Board of Education", font=("Arial", 15)).grid(row=5)
Label(master, text="Specialization in Higher Secondary Education", font=("Arial", 15)).grid(row=6)
Label(master, text="Degree Percentage", font=("Arial", 15)).grid(row=7)
Label(master, text="Under Graduation(Degree type)- Field of degree education", font=("Arial", 15)).grid(row=8)
Label(master, text="Work Experience", font=("Arial", 15)).grid(row=9)
Label(master, text="Enter test percentage", font=("Arial", 15)).grid(row=10)
Label(master, text="Branch specialization", font=("Arial", 15)).grid(row=11)
Label(master, text="MBA percentage", font=("Arial", 15)).grid(row=12)

clicked = StringVar()
options = ["Male", "Female"]
clicked1 = StringVar()
options1 = ["Central", "Others"]
clicked2 = StringVar()
options2 = ["Science", "Commerce", "Arts"]
clicked3 = StringVar()
options3 = ["Sci&Tech", "Comm&Mgmt", "Others"]
clicked4 = StringVar()
options4 = ["Yes", "No"]
clicked5 = StringVar()
options5 = ["Mkt&HR", "Mkt&Fin"]
clicked6 = StringVar()
options6 = ["Central", "Others"]

e1 = OptionMenu(master, clicked, *options)
e1.configure(width=13)
e2 = Entry(master)
e3 = OptionMenu(master, clicked1, *options1)
e3.configure(width=13)
e4 = Entry(master)
e5 = OptionMenu(master, clicked6, *options6)
e5.configure(width=13)
e6 = OptionMenu(master, clicked2, *options2)
e6.configure(width=13)
e7 = Entry(master)
e8 = OptionMenu(master, clicked3, *options3)
e8.configure(width=13)
e9 = OptionMenu(master, clicked4, *options4)
e9.configure(width=13)
e10 = Entry(master)
e11 = OptionMenu(master, clicked5, *options5)
e11.configure(width=13)
e12 = Entry(master)

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)
e3.grid(row=3, column=1)
e4.grid(row=4, column=1)
e5.grid(row=5, column=1)
e6.grid(row=6, column=1)
e7.grid(row=7, column=1)
e8.grid(row=8, column=1)
e9.grid(row=9, column=1)
e10.grid(row=10, column=1)
e11.grid(row=11, column=1)
e12.grid(row=12, column=1)

buttonFont = font.Font(family='Helvetica', size=16, weight='bold')
Button(master, text='Predict', height=1, width=8, activebackground='#00ff00', font=buttonFont, bg='black',
       fg='white', command=show_entry_fields).grid()

mainloop()
