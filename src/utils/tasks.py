import json
from datetime import datetime, timedelta

from retrievers import (retrieve_parts, retrieve_car_details, 
                        diagnose_car_problem, estimate_repair_cost)




class CarCareCoordinator:
    def __init__(self):
        """Initialize the CarCareCoordinator class."""
        pass

    def retrieve_car_details(self, make: str, model: str, year: int) -> str:
        """Retrieves the make, model, and year of the car and return the common issues if any."""
        car_details = self.get_car_model_info(0, make, model, year)  # Using 0 for mileage to get general details
        if car_details:
            return f"{year} {make} {model} - Common Issues: {', '.join(car_details['common_issues'])}"
        return f"{year} {make} {model} - No common issues found."

    def get_car_model_info(self, mileage: int, car_make: str, car_model: str, car_year: int) -> dict:
        """Retrieve car model information from cars_models.json."""
        with open('cars_models/cars_models.json', 'r') as file:
            car_models = json.load(file)

        for car in car_models:
            if (car['car_make'].lower() == car_make.lower() and car['car_model'].lower() == car_model.lower() and car['car_year'] == car_year):
                return car
        return {}

    def comprehensive_diagnosis(self, symptoms: str) -> str:
        """Provides a comprehensive diagnosis including possible causes, estimated costs, and required parts."""
        possible_causes = diagnose_car_problem(symptoms)
        likely_cause = possible_causes[0] if possible_causes else "Unknown issue"
        estimated_cost = estimate_repair_cost(likely_cause)
        required_parts = retrieve_parts(likely_cause)

        report = "Comprehensive Diagnosis Report:\n\n"
        report += f"Symptoms: {symptoms}\n\n"
        report += f"Possible Causes:\n{possible_causes}\n\n"
        report += f"Most Likely Cause: {likely_cause}\n\n"
        report += f"Estimated Cost:\n{estimated_cost}\n\n"
        report += f"Required Parts:\n{required_parts}\n\n"
        report += "Please note that this is an initial diagnosis. For accurate results, please consult with our professional mechanic."
        return report

    def plan_maintenance(self, mileage: int, car_make: str, car_model: str, car_year: int) -> str:
        """Creates a comprehensive maintenance plan based on the car's mileage and details."""
        car_details = self.retrieve_car_details(car_make, car_model, car_year)
        car_model_info = self.get_car_model_info(mileage, car_make, car_model, car_year)

        plan = f"Maintenance Plan for {car_year} {car_make} {car_model} at {mileage} miles:\n\n"
        plan += f"Car Details: {car_details}\n\n"

        if car_model_info:
            plan += "Common Issues:\n"
            for issue in car_model_info['common_issues']:
                plan += f"- {issue}\n"
            plan += f"\nEstimated Time: {car_model_info['estimated_time']}\n\n"
        else:
            plan += "No specific maintenance tasks found for this car model and mileage.\n\n"

        plan += "Please consult with our certified mechanic for a more personalized maintenance plan."
        return plan

    def create_calendar_invite(self, event_type: str, car_details: str, duration: int = 60) -> str:
        """Simulates creating a calendar invite for a car maintenance or repair event."""
        event_date = datetime.now() + timedelta(days=7)
        event_time = event_date.replace(hour=10, minute=0, second=0, microsecond=0)

        invite = "Calendar Invite Created:\n\n"
        invite += f"Event: {event_type} for {car_details}\n"
        invite += f"Date: {event_time.strftime('%Y-%m-%d')}\n"
        invite += f"Time: {event_time.strftime('%I:%M %p')}\n"
        invite += f"Duration: {duration} minutes\n"
        invite += "Location: Your Trusted Auto Shop, 123 Main St, Bengaluru, India\n\n"
        return invite

    def coordinate_car_care(self, query: str, car_make: str, car_model: str, car_year: int, mileage: int) -> str:
        """Coordinates overall car care by integrating diagnosis, maintenance planning, and scheduling."""
        car_details = retrieve_car_details(car_make, car_model, car_year)

        # Check if it's a problem or routine maintenance
        if "problem" in query.lower() or "issue" in query.lower():
            diagnosis = self.comprehensive_diagnosis(query)
            plan = f"Based on your query, here's a diagnosis:\n\n{diagnosis}\n\n"

            likely_cause = diagnosis.split("Most Likely Cause:")[1].split("\n")[0].strip()
            invite = self.create_calendar_invite(f"Repair: {likely_cause}", car_details)
            plan += f"I've prepared a calendar invite for the repair:\n\n{invite}\n\n"
        else:
            maintenance_plan = self.plan_maintenance(mileage, car_make, car_model, car_year)
            plan = f"Here's your maintenance plan:\n\n{maintenance_plan}\n\n"

            next_task = maintenance_plan.split("Task:")[1].split("\n")[0].strip()
            invite = self.create_calendar_invite(f"Maintenance: {next_task}", car_details)
            plan += f"I've prepared a calendar invite for your next maintenance task:\n\n{invite}\n\n"

        plan += "Remember to consult with a professional mechanic for personalized advice and service."
        return plan