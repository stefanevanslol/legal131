from openai import AsyncOpenAI
import os
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AIAnalyzer:
    def __init__(self, api_key: str = None):
        # Hardcoded for debugging purposes as requested
        self.api_key = "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"
        if not self.api_key:
             # In a real app, you might raise an error or warn
             pass
        # Initialize the new v1.0 client
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def analyze_medical_records(self, text: str) -> Dict[str, Any]:
        """
        Analyzes the extracted text from medical records to find key information.
        """
        # logger.info(f"Analyzing text length: {len(text)}")
        if not self.api_key:
            logger.error("No API Key found in AIAnalyzer")
             # print("DEBUG: No API Key found in AIAnalyzer") # Removed to avoid OSError
            return {"error": "OpenAI API Key not configured"}
        
        # logger.info("Calling OpenAI...")

        system_prompt = """
        You are an expert legal nurse consultant assisting an injury lawyer. Your task is to analyze medical records and specific data to populate a Demand Letter Template.
        
        You must return a valid JSON object where the keys match the variables in the template EXACTLY.
        
        Here is the mapping of Variable Names to the Context they appear in the letter. Use this context to understand what content to generate:
        ----------------------------------------------------------------
        "currentDate": The current date. Should be formatted like this: "January 1, 2023"
        "LORHeader": The header for the letter of request. Should be formatted like this: "Sent via facsimile to * 202-354-5295*" (example)
        "LORBody": The body for the letter of request. Should be formatted like this: "GEICO
ATTN: Sarah Newman
PO Box 9091 
Macon, GA 31208
" (example)
        "yourInsuredName": Name of the policyholder of the at-fault party. 
        "ClaimNo ": The insurance claim number. (Note the trailing space if present in key).
        "DateOfLoss": The date the accident occurred.
        "clientName": Full name of the client/patient.
        "refferToClient": How the client should be referred to (e.g., "Mr. John Doe" or "Ms. Jane Smith").
        
        "medicalFacility": Name of the primary medical facility visited.
        "TreatingPhysician": Name of main doctor/physician.
        "TypeTreatment": Type of treatment received (e.g., "Chiropractic Care", "Physical Therapy").
        "DatesOfTreaments": Date range of treatments (e.g., "January 1, 2023 through March 15, 2023").
        
        "complaintsByclient": A List or Paragraph describing the specific physical complaints reported by the client (e.g. "Severe neck pain radiating to shoulder, lower back stiffness"). Example: "Mr. John Does presented to Dr. Jane Doe, D.C., on May 20, 2024, with complaints of headaches, neck pain radiating into traps, upper back pain, mid back pain, lower back pain that radiates down his left leg into his foot, and right knee pain. After examining Mr. John Doe, Dr. Jonas Doe recommended continued chiropractic care and ordered an MRIs of the lumbar and cervical spine. Mr. Natale continues to receive conservative care for his injuries with Dr. Tinari.
        "TreatmentsAndDiagnosses": A detailed section describing the initial diagnoses and the treatment plan derived from the records. Example: Cervical MRI
"Cervical MRI
Impression:

There is loss of the normal lordotic curvature of the cervical spine.
There is edema seen within the odontoid and the clivus which can be seen with whiplash associated disorder and acute ligamentous injury.
At C3-4, there is bulging of the disc. This results in an anterior impression on the thecal sac. Mild neural foraminal stenosis.
At C4-5, there is bulging of the disc. This results in an anterior impression on the thecal sac. Mild neural foraminal stenosis.
At C6-7, there is a posterior disc herniation that indents the anterior surface of the thecal sac with moderate spinal canal stenosis with an AP dimension of the spinal canal of 8 mm.

Lumbar MRI
Impression:

At L3-4, there is bulging of the disc. This results in an anterior impression on the thecal sac. 
At L4-5, there is bulging of the disc. This results in an anterior impression on the thecal sac. Mild spinal canal stenosis. Mild neural foraminal stenosis. Bilateral facet osteoarthritis. 
At L5-S1, there is a posterior central/left paracentral disc herniation which pushes on the descending nerve roots, particularly the left descending nerve roots with T2 hyperintense signal seen within the posterior disc from edema and associated annular fissure. There is severe spinal canal stenosis. Moderate left neural foraminal stenosis. Mild right neural foraminal stenosis. There is edema seen in the interspinous ligament from interspinous ligament tear.

When generating this part of the document, please make important parts bold enclosing it with **. For example: At **L3-4**, there is bulging of the disc. This results in an anterior impression on the thecal sac.
        "TreatmentsAndDiagnosses2": Continuation of treatment description, progress notes, or additional diagnoses found later.
        
        "clientDescription": A narrative description of the client (e.g. "Mr. Doe, a 45-year-old Male").
        "clientLastName": The client's last name (e.g. "Mr.Doe's").
        "clientsProblems": Description of persistent problems/impairments (e.g. "complained of sleeplessness and inability to lift heavy objects").
        
        "medicalTreamentCostAndPsysican": A tab-separated or list format string detailing each provider, dates of service, and cost. Example: Tinari Chiropractic:				$7,553.12		$6,593.78	
Chiropractic Therapy			$12,000 – $14,000 per year	Dr. Dominick Tinari, D.C.
Pain Management/Surgery		$196,000			Dr. Charles Davis, M.D.
should be formatted EXACTLY as shown above. nothing more nothing less
        "PricingStructure": Example: 
        Tinari Chiropractic:				$7,553.12		$6,593.78	
        Tampa Bay Imaging:				$3,700.00		$457.94
        360 Ortho and Spine:				$30,314.00		$28,579.50
        Davis Spine & Orthopaedics:			$1,038.00		$1,038.00	
        "totalBilled": The sum total of all medical expenses (e.g. "$14,500.00"). 
        "totalOutStand": The total outstanding balance (can be same as total billed if unknown).
        
        "surgicalRecommendations": Any surgical recommendations mentioned. If none, state "No surgical recommendations indicated at this time."
        "ListOfMedicalRecords": A simple list of the documents reviewed. Example:
        Medical Records and Medical Specials:
Tinari Chiropractic	
Tampa Bay Imaging 
360 Ortho and Spine
Davis Spine & Orthopaedics
should be formatted EXACTLY as shown above. nothing more nothing less
        ----------------------------------------------------------------
        


        Analyze the provided text and populate these fields carefully. Formatting matters.
        Return ONLY valid JSON.
        """

        # Truncate text if too long (handling token limits roughly)
        truncated_text = text[:100000] # Increased limit for GPT-4o context (128k supported) 

        try:
            # Use new v1.0 syntax
            response = await self.client.chat.completions.create(
                model="gpt-5", # Using a known model string just in case gpt-5 is not valid yet
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze these records:\n\n{truncated_text}"}
                ],
                response_format={"type": "json_object"},
                timeout=180.0 # 3 minutes timeout
            )
            
            content = response.choices[0].message.content
            # logger.info(f"OpenAI Raw Content: {content[:500]}...") # Log first 500 chars to avoid huge logs
            # print(f"DEBUG: OpenAI Raw Content:\n{content}") # Removed to avoid potential issues
            
            # Sanitize content (remove markdown code blocks if present)
            if content.startswith("```json"):
                content = content.replace("```json", "").replace("```", "")
            elif content.startswith("```"):
                 content = content.replace("```", "")
            
            return json.loads(content)
        except Exception as e:
            logger.error(f"OpenAI Error: {e}")
            # print(f"DEBUG: OpenAI Error: {e}", flush=True)
            return {"error": str(e)}
