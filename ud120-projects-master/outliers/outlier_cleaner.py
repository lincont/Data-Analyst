#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where
        each tuple is of the form (age, net_worth, error).
    """

#    cleaned_data = []
#    i = 0
#
#    ### your code goes here
#    for i in range(len((predictions, ages, net_worths))):
#        errors = float(predictions[i])/net_worths[i]
#        if errors < .9:
#            cleaned_data.append(ages[i], net_worths[i], errors)
#        i += 1

#    return cleaned_data
    cleaned_data = []
    errors = (predictions - net_worths)/net_worths

    for i in range(len(errors)):
        if errors[i] < .9:
            cleaned_data.append((ages[i], net_worths[i], errors[i]))

    return cleaned_data
