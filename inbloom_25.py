import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from PIL import Image, ImageEnhance
import os

# Step 1: Dataset
def generate_dataset():
    participants = []
    events = ["Treasure Hunt", "Music", "Football", "Gaming", "Photography", "Chess", "Quiz", "Debate", "Catch The Flag", "Cricket"]
    colleges = ["Christ University Bangalore", "Kristu Jayanti College", "Jyoti Niwas College", "BIT Mesra", "IIT Bombay","BITS Pilani"]
    states = ["Karnataka", "West Bengal", "Tamil Nadu", "Jharkhand", "Rajasthan","Maharashtra"]
    
    feedback_options = [
        "Amazing event!", "Loved it", "Could be better", "Fantastic experience", "Not great", "Management was Good",
        "Behaviour of Volunteers was very nice", "Liked the Refreshments", "Some events could have been better",
        "Pathetic", "The judges were Fair", "Good Decoration", "Awesome", "Internet and Lab Systems were working very nice","Good Campus","Flabbergasting","Worth It","Superb!! , Will attend this fest again next year","10 on 10","Teriffic"
    ]
    
    for i in range(250):
        participant = {
            "Participant_ID": i + 1,
            "Name": f"Participant_{i+1}",
            "College": random.choice(colleges),
            "State": random.choice(states),
            "Event": random.choice(events),
            "Day": random.randint(1, 5),
            "Feedback": random.choice(feedback_options)
        }
        participants.append(participant)
    
    return pd.DataFrame(participants)

df = generate_dataset()

# Step 2: Build Streamlit Dashboard
st.title("INBLOOM '25 - Participation Analysis Dashboard")
st.title("The Generated Dataset ")
df

# Sidebar Filters
st.sidebar.title("Visualize the Event here")
selected_event = st.sidebar.selectbox("Select Event", ["All"] + df["Event"].unique().tolist())
selected_college = st.sidebar.selectbox("Select College", ["All"] + df["College"].unique().tolist())
selected_state = st.sidebar.selectbox("Select State", ["All"] + df["State"].unique().tolist())

# Apply Filters
df_filtered = df.copy()
if selected_event != "All":
    df_filtered = df_filtered[df_filtered["Event"] == selected_event]
if selected_college != "All":
    df_filtered = df_filtered[df_filtered["College"] == selected_college]
if selected_state != "All":
    df_filtered = df_filtered[df_filtered["State"] == selected_state]

# Step 3: Data Visualization
st.subheader("Participation Trends")

# Event-wise Participation
fig, ax = plt.subplots()
sns.countplot(y=df_filtered["Event"], order=df_filtered["Event"].value_counts().index, palette="viridis", ax=ax)
ax.set_title("Event-wise Participation")
st.pyplot(fig)

# Day-wise Participation
fig, ax = plt.subplots()
sns.countplot(x=df_filtered["Day"], palette="coolwarm", ax=ax)
ax.set_title("Day-wise Participation")
st.pyplot(fig)

# College-wise Participation
fig, ax = plt.subplots()
sns.countplot(y=df_filtered["College"], order=df_filtered["College"].value_counts().index, palette="magma", ax=ax)
ax.set_title("College-wise Participation")
st.pyplot(fig)

# State-wise Participation
fig, ax = plt.subplots()
sns.countplot(y=df_filtered["State"], order=df_filtered["State"].value_counts().index, palette="plasma", ax=ax)
ax.set_title("State-wise Participation")
st.pyplot(fig)

# Step 4: Feedback Analysis
st.subheader("Feedback Analysis")

# Generate Word Cloud
feedback_text = " ".join(df_filtered["Feedback"].astype(str))
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(feedback_text)
fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis("off")
st.pyplot(fig)

# Event-wise Feedback Comparison
st.subheader("Event-wise Feedback Comparison")

# Group feedback by event
event_feedback_counts = df.groupby(["Event", "Feedback"]).size().unstack().fillna(0)

# Plot event-wise feedback distribution
fig, ax = plt.subplots(figsize=(10, 6))
event_feedback_counts.plot(kind="bar", stacked=True, colormap="tab10", ax=ax)
ax.set_title("Feedback Distribution for Each Event")
ax.set_ylabel("Count of Feedback")
ax.set_xlabel("Event")
ax.legend(title="Feedback", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig)




# Step 5: Image Processing
st.subheader("Event Photos - Day-wise Gallery")

# Preloaded images for each day
image_paths = {
    1: ["img1.jpg", "img2.jpg", "img3.jpg"],
    2: ["img1.jpg", "img3.jpg", "img2.jpg"],
    3: ["img2.jpg", "img1.jpg", "img3.jpg"],
    4: ["img3.jpg", "img2.jpg", "img1.jpg"],
    5: ["img1.jpg", "img3.jpg", "img2.jpg"]
}

#  Select Day
selected_day = st.selectbox("Select Day to View Images", list(image_paths.keys()))

# Display images in a grid format
st.subheader(f"Images from Day {selected_day}")

cols = st.columns(3)  # 3 images per row
for index, img_path in enumerate(image_paths[selected_day]):
    try:
        img = Image.open(img_path)
        with cols[index % 3]:  # Arrange images in a grid
            st.image(img, caption=f"Day {selected_day} - Image {index+1}", use_column_width=True)
    except FileNotFoundError:
        with cols[index % 3]:
            st.warning(f"Image {img_path} not found.")






# Step 6: Image Processing with Advanced Options
st.subheader("Image Processing")
uploaded_file = st.file_uploader("Upload an Image for Processing", type=["jpg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    # Image Processing Options
    option = st.selectbox("Choose Image Processing", [
        "Original", "Grayscale", "Enhance Contrast", "Rotate", "Color Grading", "Edge Detection"
    ])

    # Apply Grayscale
    if option == "Grayscale":
        image = image.convert("L")

    # Enhance Contrast
    elif option == "Enhance Contrast":
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)

    # Rotate Image
    elif option == "Rotate":
        angle = st.radio("Select Rotation Angle", [90, 180, 270])
        image = image.rotate(angle)

    

    # Color Grading (Brightness, Contrast, Sharpness)
    elif option == "Color Grading":
        brightness = st.slider("Brightness", 0.5, 2.0, 1.0)
        contrast = st.slider("Contrast", 0.5, 2.0, 1.0)
        sharpness = st.slider("Sharpness", 0.5, 2.0, 1.0)
        
        image = ImageEnhance.Brightness(image).enhance(brightness)
        image = ImageEnhance.Contrast(image).enhance(contrast)
        image = ImageEnhance.Sharpness(image).enhance(sharpness)

    # Edge Detection
    elif option == "Edge Detection":
        from PIL import ImageFilter
        image = image.convert("L").filter(ImageFilter.FIND_EDGES)

    # Display Processed Image
    st.image(image, caption=f"Processed Image - {option}", use_column_width=True)





# Step 7: Run the Streamlit App
if __name__ == "__main__":
    st.write("INBLOOM '25 Data Dashboard is Running")
