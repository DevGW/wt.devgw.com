def convert_weight(weight, from_unit, to_unit):
    """
    Convert weight between kg and lbs.

    Args:
        weight (float): The weight value.
        from_unit (str): 'kg' or 'lbs'.
        to_unit (str): 'kg' or 'lbs'.

    Returns:
        float: The converted weight.
    """
    if from_unit == to_unit:
        return weight
    if from_unit == 'kg' and to_unit == 'lbs':
        return weight * 2.20462
    if from_unit == 'lbs' and to_unit == 'kg':
        return weight / 2.20462
    raise ValueError("Invalid conversion units.")


def convert_height(height, from_unit, to_unit):
    """
    Convert height between cm and inches.

    Args:
        height (float): The height value.
        from_unit (str): 'cm' or 'inches'.
        to_unit (str): 'cm' or 'inches'.

    Returns:
        float: The converted height.
    """
    if from_unit == to_unit:
        return height
    if from_unit == 'cm' and to_unit == 'inches':
        return height / 2.54
    if from_unit == 'inches' and to_unit == 'cm':
        return height * 2.54
    raise ValueError("Invalid conversion units.")


def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI given weight in kg and height in cm.

    Args:
        weight_kg (float): Weight in kilograms.
        height_cm (float): Height in centimeters.

    Returns:
        float: The BMI.
    """
    height_m = height_cm / 100.0
    return weight_kg / (height_m ** 2)


def bmi_category(bmi):
    """
    Determine BMI category.

    Args:
        bmi (float): BMI value.

    Returns:
        str: Category label.
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obesity"


def calculate_weekly_target(latest_weight, goal_weight, current_date, target_date):
    """
    Calculate the required weekly weight loss to reach the goal weight.

    Args:
        latest_weight (float): Latest weight in kg.
        goal_weight (float): Target weight in kg.
        current_date (date): Current date.
        target_date (date): Goal target date.

    Returns:
        float: Required weekly weight loss in kg.
    """
    total_weeks = max((target_date - current_date).days / 7, 1)
    weight_diff = latest_weight - goal_weight
    return weight_diff / total_weeks
