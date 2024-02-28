# Using various NLP models to classify whether a string is an entity

import spacy # SpaCy 3.7
import nltk
import os
import csv
import flair

class NameClassifier:
    """ This class uses three separate NER models to determine whether a string is a name """

    filename = 'name_classification.csv'
    filepath = os.path.join('user_data', filename)

    # Load entities
    spacyNLP = spacy.load('en_web_core_lg')

    # Write order
    rows = ['Original Text', 'Spacy Total', 'Spacy Persons', 'Spacy Decision', 'Stanford Total', 'Stanford Persons', 'Stanford Decision']

    def __init__(self, text: str):

        # Using the SpaCy model
        spacyData = self._spacyNER(text)
        spacyEntTotal, spacyEntPersons, spacyDecision = spacyData['ent_total'], spacyData['ent_persons'], spacyData['is_person']
        # Using the NLTK stanford model
        stanfordData = self._stanfordNER(text)
        stanfordEntTotal, stanfordEntPersons, stanfordDecision = stanfordData['ent_total'], stanfordData['ent_persons'], stanfordData['is_person']
        # Using the Flair model
        flairData = self._flairNER(text)
        flairEntTotal, flairEntPersons, flairDecision = flairData['ent_total'], flairData['ent_persons'], flairData['is_person']

        # Write all the data to a file.
        self.write_to_file(text, [spacyEntTotal, spacyEntPersons, spacyDecision], [stanfordEntTotal, stanfordEntPersons, stanfordDecision], [flairEntTotal, flairEntPersons, flairDecision])

        # The logic
        self.decision = all([spacyDecision, stanfordDecision, flairDecision])


    def _spacyNER(self, text: str) -> dict:
        """ Determines whether or not spacy believes this text is a name."""
        doc = self.spacyNLP(text)
        ents = [ent for ent in doc]
        ents_persons = [ent for ent in doc if ent.ent_type_ == 'PERSON']
        return {'ent_total': len(ents), 'ent_persons': len(ents), 'is_person': bool(ents_persons)}

    def _stanfordNER(self, text: str) -> dict:
        """ Determines whether or not NLTK - python believes this text is a name."""
        tokens = nltk.word_tokenize(text)
        tags = nltk.pos_tag(tokens)
        entities = nltk.ne_chunk(tags)
        ents = []
        ents_persons = []
        for entity in entities:
            ents.append(entity)
            if hasattr(entity, 'label') and entity.label == 'PERSON':
                ents_persons.append(entity)

        return {'ent_total': len(ents), 'ent_persons': len(ents_persons), 'is_person': bool(ents_persons)}

    def _flairNER(self, text):
        """ Uses flair's NER to decide if this is a name"""
        ner = flair.modes.SequenceTagger.load("ner-fast")
        ner_predictions = ner.predict(text)

        # Get entities
        ents = []
        ents_persons = []
        for pred in ner_predictions:
            ents.append(pred)
            if pred == "PERSON":
                ents_persons.append(pred)

        return {'ent_total': len(ents), 'ent_persons': len(ents_persons),
                'is_person': bool(ents_persons)}

    def write_to_file(self, text: str, spacyRow: list, stanfordRow: list, flairRow: list) -> None:
        """ Write user data to a CSV. May be useful in the future."""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as f:
                writer = csv.writer(f)
                writer.writerow(self.rows)

        with open(self.filepath, "a") as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerow([text] + spacyRow + stanfordRow + flairRow)

    def get_decision(self) -> bool:
        """ Return whether or not this is determined to be a name."""
        return self.decision