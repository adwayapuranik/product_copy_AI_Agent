import boto3
import json
import base64
import pandas as pd
import time

from tqdm import tqdm
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from product_copy_agent.utils import get_bedrock_invoke_payload
from product_copy_agent.prompts import (
    CHAIN_OF_THOUGHT_INSTRUCTIONS_PROMPT,
    CHAIN_OF_THOUGHT_PRODUCT_COPY_PROMPT,
)

BODY = "body"
CONTENT = "content"
MESSAGES = "messages"
PRODUCT_COPY = "productcopy"
TEXT = "text"
VALIDATED_PRODUCT_COPY = "validated_product_copy"
VARIANT_GROUP_CODE = "variantGroupCode"


class BedrockInvokeModel:
    def __init__(self, model_id: str = "anthropic.claude-3-5-sonnet-20240620-v1:0", region_name='us-east-1'):
            """
            Initialize the processor with AWS clients and model configuration
            
            Args:
                model_id (str): The Bedrock model ID to use for inference
            """
            self.bedrock_client = boto3.client('bedrock-runtime', region_name=region_name)
            self.model_id = model_id

    def bedrock_invoke(self, prompt: str) -> str:
        """Method to do bedrock invoke"""
        payload = get_bedrock_invoke_payload()

        payload[MESSAGES][0][CONTENT][0][TEXT] = prompt

        response = self.bedrock_client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(payload)
        )

        try:
            response_body = json.loads(response[BODY].read())
            result = response_body[CONTENT][0][TEXT]
        except Exception as e:
            raise Exception("Bedrock Invoke Has Failed.")
        
        return result

    def _generate_new_dynamic_prompt(self, file_content: str):
        """generates the new dynamic prompt based on the instructions"""
        prompt = CHAIN_OF_THOUGHT_INSTRUCTIONS_PROMPT.format(
            raw_instructions=file_content
        )
        
        product_copy_instructions = self.bedrock_invoke(prompt)

        return product_copy_instructions

    def process_single_row(self, product_copy: str, latest_instructions: str, ) -> Dict:
        """Process a single row from the DataFrame
        Args:
            row (pd.Series): A single row from the DataFrame            
        Returns:
            Dict: Processing results for the row
        """
        try:
            prompt = CHAIN_OF_THOUGHT_PRODUCT_COPY_PROMPT.format(
                framework=latest_instructions,
                product_copy=product_copy
            )
            
            validated_product_copy = self.bedrock_invoke(prompt)
            time.sleep(0.1)

            return validated_product_copy
            
        except Exception as e:
            print(f"bedrock invoke failed with error: {e}")

    def run_batch_invoke(self, lastest_instructions: str, input_data: list, max_workers: int = 3):
        """
        Process the entire DataFrame and save results to CSV
        
        Args:
            input_data (list): Jsonl list with prompts
            max_workers (int): Number of concurrent workers
        """
        results = []
        
        with ThreadPoolExecutor(max_workers = max_workers) as executor:
            future_to_variant = {}
            for row in input_data.itertuples(index=False):
                variant_code = row.variantGroupCode
                future = executor.submit(
                    self.process_single_row,
                    row.productcopy,
                    lastest_instructions,
                )
                future_to_variant[future] = variant_code

            results = []
            for future in tqdm(as_completed(future_to_variant), total=len(future_to_variant), desc="Processing rows"):
                variant_code = future_to_variant[future]
                try:
                    transformed_copy = future.result()
                    if transformed_copy:
                        results.append({
                        VARIANT_GROUP_CODE: variant_code,
                        VALIDATED_PRODUCT_COPY: transformed_copy
                    })
                except Exception as e:
                    raise Exception(f"Error processing {variant_code}: {e}")
        return results