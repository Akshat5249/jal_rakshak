"""
Example Vercel serverless function for dashboard summary.
This shows how to convert a Flask route to a serverless function.
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path to import shared utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from api._shared import load_data, convert_nan_to_none
except ImportError:
    # Fallback if running locally
    from _shared import load_data, convert_nan_to_none


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET request for dashboard summary"""
        try:
            # Load data
            processed_data_df = load_data()
            
            if processed_data_df.empty:
                response_data = {}
            else:
                # Calculate summary statistics
                total_reports = len(processed_data_df)
                active_alerts = len([row for idx, row in processed_data_df.iterrows() if row["WaterQuality_Label"] == 1])
                high_risk_villages = processed_data_df[processed_data_df["WaterQuality_Label"] == 1]["Location"].nunique()
                new_reports_24h = int(total_reports * 0.1)
                
                response_data = {
                    "totalReportsToday": total_reports,
                    "activeAlerts": active_alerts,
                    "highRiskVillages": high_risk_villages,
                    "newReports24h": new_reports_24h
                }
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(convert_nan_to_none(response_data)).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
