import markovify
import random

# Scary texts for Markov chain training
SCARY_TEXTS = """
The shadows in {city} whisper secrets of the damned. Those who listen never return the same.
Beware the October moon in {city}, for it reveals what should remain hidden.
Children of {city} speak of the pale lady who walks when the church bell tolls thirteen.
In the fog of {city}, shapes move that have no business in our world.
The old cemetery in {city} has one grave that was never meant to be opened.
They say in {city} that if you hear your name called by the wind, don't answer.
The abandoned factory in {city} echoes with laughter that stopped seventy years ago.
When the clock strikes midnight in {city}, count the faces in the window. If there's one too many, run.
The river through {city} carries more than water after the autumn equinox.
Residents of {city} lock their doors extra tight on Halloween night, and for good reason.
The legend says that every Halloween, one person from {city} disappears into the mist forever.
"""

def generate_scary_prediction(city):
    try:
        # Train Markov model
        text_model = markovify.Text(SCARY_TEXTS)
        
        # Generate multiple sentences and pick one
        predictions = []
        for _ in range(10):
            try:
                pred = text_model.make_sentence()
                if pred:
                    predictions.append(pred.replace("{city}", city))
            except:
                continue
        
        if predictions:
            return random.choice(predictions)
        else:
            return f"The spirits of {city} grow restless this Halloween night..."
    except:
        return f"Dark forces gather in {city}... Beware the shadows!"