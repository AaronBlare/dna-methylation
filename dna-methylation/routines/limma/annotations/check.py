def check_condition(annotations, annotations_dict, index):

    is_passed = True

    for key, positive_values in annotations.positive_dict.items():
        if key in annotations_dict:
            target_values = annotations_dict[key][index]

            if 'empty' in positive_values:
                if len(target_values) > 0:
                    is_passed = False
                    break

            elif 'non-empty' in positive_values:
                if len(target_values) == 0:
                    is_passed = False
                    break

            else:
                positive_values = set(positive_values)
                target_values = set(target_values)
                intersection = list(positive_values.intersection(target_values))
                if len(intersection) == 0:
                    is_passed = False

    if is_passed:
        for key, negative_values in annotations.negative_dict.items():
            if key in annotations_dict:
                target_values = annotations_dict[key][index]
                negative_values = set(negative_values)
                target_values = set(target_values)
                intersection = list(negative_values.intersection(target_values))
                if len(intersection) > 0:
                    is_passed = False

    return is_passed


def exclude_condition(annotations, annotations_dict, excluded, index):
    if annotations_dict[annotations.id_name][index][0] in excluded:
        return False
    else:
        return True


def cpg_name_condition(annotations, annotations_dict, index):
    if len(annotations_dict[annotations.id_name][index]) > 0:
        return True
    else:
        return False


def global_check(annotations, annotations_dict, excluded, index):
    is_passed = False

    if cpg_name_condition(annotations, annotations_dict, index):
        if exclude_condition(annotations, annotations_dict, excluded, index):
            if check_condition(annotations, annotations_dict, index):
                is_passed = True

    return is_passed
