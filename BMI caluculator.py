def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

def get_health_advice(category):
    advice = {
        "Underweight": "It's important to eat a healthy and balanced diet. Consider consulting a healthcare professional.",
        "Normal weight": "Great job maintaining a healthy weight! Keep following a balanced diet and regular exercise.",
        "Overweight": "You might want to consider a healthier diet and more physical activity. Talk to a healthcare professional for guidance.",
        "Obese": "It’s important to consult with a healthcare provider for advice on achieving a healthier weight."
    }
    return advice.get(category, "No advice available.")

def convert_units(weight, height, unit_system):
    if unit_system == 'imperial':
        weight = weight * 0.453592  # Convert pounds to kilograms
        height = height * 0.0254    # Convert inches to meters
    return weight, height

def input_weight_and_height():
    while True:
        try:
            weight = float(input("Enter your weight: "))
            height = float(input("Enter your height: "))
            return weight, height
        except ValueError:
            print("Invalid input. Please enter numerical values for weight and height.")

def bmi_calculator():
    print("Welcome to the Enhanced BMI Calculator!")
    
    while True:
        print("\nSelect your preferred unit system:")
        print("1. Metric (kilograms, meters)")
        print("2. Imperial (pounds, inches)")
        
        unit_choice = input("Enter 1 for Metric or 2 for Imperial: ").strip()

        if unit_choice == '1':
            unit_system = 'metric'
        elif unit_choice == '2':
            unit_system = 'imperial'
        else:
            print("Invalid choice. Please select 1 or 2.")
            continue
        
        weight, height = input_weight_and_height()
        
        if unit_system == 'imperial':
            weight, height = convert_units(weight, height, unit_system)
        
        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)
        advice = get_health_advice(category)
        
        print(f"\nYour BMI is: {bmi:.2f}")
        print(f"Based on your BMI, you are classified as: {category}")
        print(f"Health Advice: {advice}")
        
        # Ask the user if they want to calculate BMI for another person
        another_calc = input("\nWould you like to calculate BMI for another person? (yes/no): ").strip().lower()
        if another_calc not in ['yes', 'y']:
            print("Thank you for using the BMI Calculator. Stay healthy!")
            break

if __name__ == "__main__":
    bmi_calculator()
