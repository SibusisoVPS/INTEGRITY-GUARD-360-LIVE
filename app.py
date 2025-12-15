from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '''
    <html>
    <head><title>INTEGRITY-GUARD-360</title>
    <style>body{font-family:Arial;margin:0;background:#0f172a;color:white;}
    .container{max-width:1000px;margin:auto;padding:20px;}
    .header{background:#1e293b;padding:30px;border-radius:10px;margin-bottom:20px;text-align:center;}
    .btn{background:#3b82f6;color:white;padding:12px 24px;border:none;border-radius:6px;cursor:pointer;margin:10px;font-size:16px;}
    .result{background:#10b981;padding:20px;margin:20px 0;border-radius:8px;}
    .gep-score{font-size:72px;font-weight:bold;margin:20px 0;}
    </style></head>
    <body>
    <div class="container">
        <div class="header">
            <h1>🛡️ INTEGRITY-GUARD-360</h1>
            <p>German Excellence Framework v1.0 • LIVE</p>
            <button class="btn" onclick="testAPI()">✅ Test API</button>
            <button class="btn" onclick="runAssessment('ZA')">🇿🇦 South Africa</button>
            <button class="btn" onclick="runAssessment('DE')">🇩🇪 Germany</button>
            <button class="btn" onclick="runAssessment('US')">🇺🇸 USA</button>
        </div>
        <div id="result"></div>
    </div>
    <script>
    async function testAPI(){
        const r = await fetch('/api/assess');
        const d = await r.json();
        document.getElementById('result').innerHTML = 
            `<div class="result"><h3>✅ ${d.framework}</h3>
            <p>Status: ${d.status} • Version: ${d.version}</p></div>`;
    }
    
    async function runAssessment(country){
        const r = await fetch('/api/assess', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({country: country})
        });
        const d = await r.json();
        const color = d.german_excellence_percentage >= 80 ? '#10b981' : 
                     d.german_excellence_percentage >= 60 ? '#f59e0b' : '#ef4444';
        document.getElementById('result').innerHTML = 
            `<div class="result">
                <h2>🇩🇪 German Excellence Assessment</h2>
                <div class="gep-score" style="color:${color}">
                    ${d.german_excellence_percentage}%
                </div>
                <p>Country: ${d.country} • Classification: ${d.classification}</p>
                <p>${d.timestamp}</p>
            </div>`;
    }
    </script>
    </body>
    </html>
    '''

@app.route('/api/assess', methods=['GET', 'POST', 'OPTIONS'])
def assess():
    if request.method == 'OPTIONS':
        return '', 200
    
    if request.method == 'GET':
        return jsonify({
            "status": "ACTIVE",
            "framework": "German Excellence Standard v1.0",
            "version": "1.0.0",
            "endpoints": ["GET /api/assess", "POST /api/assess"]
        })
    
    data = request.json
    gep = calculate_gep(data.get('country', 'GLOBAL'))
    
    return jsonify({
        "german_excellence_percentage": gep,
        "country": data.get('country', 'GLOBAL'),
        "classification": classify_system(gep),
        "improvement_priority": "CRITICAL" if gep < 40 else "HIGH" if gep < 60 else "MEDIUM" if gep < 80 else "LOW",
        "timestamp": datetime.datetime.now().isoformat()
    })

def calculate_gep(country):
    scores = {'DE':92,'ZA':42,'US':68,'GB':72,'FR':70,'JP':75,'SG':80,'IN':38,'BR':35,'NG':28}
    return scores.get(country.upper() if country else 'GLOBAL', 50)

def classify_system(gep):
    if gep >= 90: return "GERMAN_EXCELLENCE_COMPATIBLE"
    if gep >= 80: return "NEAR_EXCELLENCE"
    if gep >= 70: return "SUBSTANTIAL_COMPETENCE"
    if gep >= 60: return "MODERATE_COMPETENCE"
    if gep >= 50: return "BASIC_FUNCTIONALITY"
    return "NEEDS_IMPROVEMENT"

if __name__ == '__main__':
    app.run(debug=True)
