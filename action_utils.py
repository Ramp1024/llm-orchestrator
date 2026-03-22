def clone_action(actions, source_action_id, new_labels):
    
    source_action = None
    
    for action in actions:
        if action["Id"] == source_action_id:
            source_action = action
            break

    if source_action is None:
        raise Exception("Source action not found")

    new_actions = []

    for label in new_labels:

        translation_key = label.upper().replace(" ", "_")

        new_action = source_action.copy()

        new_action["Id"] = source_action_id
        new_action["Label"] = label
        new_action["TranslationKey"] = translation_key

        new_actions.append(new_action)

    return new_actions


def apply_clone_operation(actions, operation):

    source = operation.sourceAction
    new_labels = operation.newLabels

    cloned_actions = clone_action(actions, source, new_labels)

    insert_index = None

    for i, action in enumerate(actions):
        if action["Id"] == source:
            print(i)
            insert_index = i
            break

    if insert_index is None:
        raise Exception("Insert location not found")

    # Remove the source action
    actions.pop(insert_index)

    for i, new_action in enumerate(cloned_actions):
        actions.insert(insert_index + i, new_action)

    return actions
