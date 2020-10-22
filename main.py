#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

import json
import time
import csv

from employeedb import EmployeeDB

# Azure Face API用モジュール
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType

PERSON_GROUP_ID = ""

class FaceRecognition():
    def __init__(self):
        settings = json.load(
            open('face-api-config.json', 'r')
        )
        # Create an authenticated FaceClient.
        self.face_client = FaceClient(
            settings.get('API_ENDPOINT'), 
            CognitiveServicesCredentials(settings.get('API_ACCESS_KEY'))
        )

    def createPersonGroup(self):
        print('Create person group '+PERSON_GROUP_ID)
        self.face_client.person_group.create(
            person_group_id=PERSON_GROUP_ID, 
            name=PERSON_GROUP_ID
        )

    def deletePersonGroup(self):
        print('Delete person group '+PERSON_GROUP_ID)
        self.face_client.person_group.delete(
            person_group_id=PERSON_GROUP_ID
        )

    def createPerson(self, name):
        print('Create person')
        person = self.face_client.person_group_person.create(PERSON_GROUP_ID, name)
        return person.person_id

    def getPersonList(self):
        print('get person list')
        persons = self.face_client.person_group_person.list(PERSON_GROUP_ID)
        for person in persons:
            print(person)

    def getPerson(self, personId):
        print('Create person '+personId)
        person = self.face_client.person_group_person.get(PERSON_GROUP_ID, personId)
        print(person)

    def setPersonImage(self, personId, imagePath):
        print('Set person image '+imagePath)
        image = open(imagePath, 'r+b')
        self.face_client.person_group_person.add_face_from_stream(
            PERSON_GROUP_ID, personId, image)

    def train(self):
        # Train the person group
        self.face_client.person_group.train(PERSON_GROUP_ID)

        print('Training the person group...')
        while (True):
            training_status = self.face_client.person_group.get_training_status(PERSON_GROUP_ID)
            print("Training status: {}.".format(training_status.status))
            if (training_status.status is TrainingStatusType.succeeded):
                break
            elif (training_status.status is TrainingStatusType.failed):
                sys.exit('Training the person group has failed.')
            time.sleep(1)

    def getPersonIdFromImage(self, faceImage):
        print(faceImage)
        image = open(faceImage, 'r+b')

        # Detect faces
        face_ids = []
        faces = face_client.face.detect_with_stream(image)
        for face in faces:
            print(face)
        #    face_ids.append(face.face_id)

        #return face_client.face.identify(face_ids, PERSON_GROUP_ID)


def main():
    fr = FaceRecognition()

    # reset person group
    fr.deletePersonGroup()
    fr.createPersonGroup()
    
    db = EmployeeDB()
    db.deleteAll()
    
    with open('file/person_list.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 5 or not row[0] or not row[1] or not row[2] or not row[3] or not row[4]:
                continue

            time.sleep(0.2)

            employee_id = row[0]
            name        = row[1]
            department  = row[2]
            position    = row[3]
            image_path  = "./file/" + row[4]

            person_id = fr.createPerson(employee_id)
            fr.setPersonImage(person_id, image_path)

            db.insertEmployee(int(employee_id), name, department, position)
            db.insertPersonID(int(employee_id), person_id)
            db.insertImages(int(employee_id), 1, image_path)

    fr.train()
    fr.getPersonList()

if __name__ == "__main__":
    main()

