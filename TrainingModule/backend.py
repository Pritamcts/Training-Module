from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

# Initialize a global variable to hold the database connection
db_connection = None
# Function to establish a database connection if not already connected
def get_db_connection():
    global db_connection
    if db_connection is None:
        try:
            db_connection = psycopg2.connect(
               dbname="PANNADB",
               user="postgres",
               password="root",
               host="localhost",
               port="5432"
            )
        except psycopg2.Error as e:
            print("Error connecting to PostgreSQL database:", e)
    return db_connection


    
@app.route('/insert_db', methods=['GET'])

def insert_db():
    data=request.json
    prompt = data.get('prompt')
    refined_prompt = data.get('refined_prompt')
    result=data.get('summary')
    userid=data.get('userid')
    current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        # Get the database connection
        conn = get_db_connection()
        
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        # Create a cursor object
        cursor = conn.cursor()
        # Update rating and feedback in the database
        query = """INSERT INTO prompt_audit (time,prompt,refined_prompt,response,feedback,feedback_comment,channel) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
        cursor.execute(query, (current_time,prompt,refined_prompt,result,'Null','Null','training'))

        # Commit the transaction
        conn.commit()
        
        # Close the cursor
        cursor.close()
        
        return jsonify ({"message":'Submitted'})
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500
    
# Endpoint to handle storing feedback
  
@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    prompt = data.get('prompt')
    refined_prompt = data.get('refined_prompt')
    result=data.get('summary')
    rating = str(data.get('rating'))
    feedback = data.get('feedback')
    try:
        # Get the database connection
        conn = get_db_connection()
        
        if conn is None:
            return jsonify({"error": "Failed to connect to database"}), 500
        
        # Create a cursor object
        cursor = conn.cursor()
        query = """UPDATE prompt_audit SET feedback=%s, feedback_comment=%s WHERE prompt=%s AND refined_prompt=%s AND response=%s"""
        cursor.execute(query, (rating,feedback,prompt,refined_prompt,result))
        # Commit the transaction
        conn.commit()
        
        # Close the cursor
        cursor.close()
        
        return jsonify({"message": "Feedback submitted successfully"})
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=5002)


