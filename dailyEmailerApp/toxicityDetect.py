from googleapiclient import discovery
import json

'''
This Script class detect the toxicity type and lable of toxicity in text
'''

class Messagefilter:
    
    #Your API TOXICITY API KEY
    API_KEY = ''
    
    #Client Connection
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=API_KEY,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
        )

    #Types of Toxicity 
    type_detect = {
        'SEVERE_TOXICITY':{},
        'INSULT':{},
        'SEXUALLY_EXPLICIT':{},
        'PROFANITY':{},
        'THREAT':{},
        'IDENTITY_ATTACK':{} 
        }

    #Format of Request
    analyze_request = {
        'comment': { 'text': "" },
        'requestedAttributes': type_detect
        }
    
    #Run the Filter of Toxicity     
    def runFilter(self,message):
        self.analyze_request['comment']['text'] = message
        try:
            response = self.client.comments().analyze(body=self.analyze_request).execute()
            return  self.detect(response)
        except Exception as e:
            print(f"Message Filter Error: {e}")
            return ''
     
    #Detect the Toxicity         
    def detect(self,attributeData):
        attributeScoreData = attributeData['attributeScores']
        dicValueType = {key:value['summaryScore']['value'] for key,value in attributeScoreData.items() if value['summaryScore']['value'] > 0.20}
        if dicValueType != {}:
            return max(zip(dicValueType.values(), dicValueType.keys()))[1]
        else:
            return ''
 
