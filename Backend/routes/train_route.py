from flask import Blueprint, request, jsonify
from bson import ObjectId
# models
from schemamodels.transcripts import TranscriptsModel
from schemamodels.qna import QnAModel

# collections
from config.db import transcripts_collection
from config.db import qna_collection

# authentication
from authentication.authentication import authentication

# trainer prompt
from train.trainer_prompt import trainer_prompt

train_bp = Blueprint('train_bp', __name__)


@train_bp.route('/add-transcript', methods=['POST'])
@authentication
def add_transcript():
    try:
        body = request.json
        influencer_id = request.environ['influencer_id']
        # check if trasncipt of the influencer already exists
        transcript = transcripts_collection.find_one(
            {"influencer_id": ObjectId(influencer_id), "transcript": body['transcript']})
        if transcript:
            return jsonify({"status": "error", "message": "Transcript already exists"}), 400
        transcript = TranscriptsModel(
            influencer_id=influencer_id, transcript=body['transcript'])
        transcripts_collection.insert_one(transcript.__dict__)
        return jsonify({"status": "success", "message": "Transcript Added"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route('/get-transcripts', methods=['GET'])
@authentication
def get_transcripts():
    influencer_id = request.environ['influencer_id']
    try:
        transcripts = list(transcripts_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        return jsonify({"status": "success", "data": transcripts}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route('/add-qnas', methods=['POST'])
@authentication
def add_qna():
    body = request.json
    influencer_id = request.environ['influencer_id']
    try:
        qna = QnAModel(influencer_id=influencer_id,
                       sample_question=body['sample_question'], sample_answer=body['sample_answer'])
        qna_collection.insert_one(qna.__dict__)
        return jsonify({"status": "success", "message": "QnA Added"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route('/get-qnas', methods=['GET'])
@authentication
def get_qna():
    influencer_id = request.environ['influencer_id']
    try:
        qnas = list(qna_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        return jsonify({"status": "success", "data": qnas}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@train_bp.route("/train", methods=['GET'])
@authentication
def train():
    influencer_id = request.environ['influencer_id']
    try:
        transcripts = list(transcripts_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        sampleQnA = list(qna_collection.find(
            {"influencer_id": ObjectId(influencer_id)}))
        prompt = trainer_prompt(sampleQnA, transcripts)
        print(prompt)
        return jsonify({"status": "success", "message": "Training Complete"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400
