def inspect_achievement(achievements, entity_type, entity, dirty_fields):
    """
    Background celery task for achievements inspection.
    """
    # Getting only achievements that have sense to be checked
    achievements = achievements.filter(
        entity_type=entity_type,
        requirements__key__in=dirty_fields.keys()
    )

    # Inspecting
    for achievement in achievements:
        achievement.logic.inspect(entity)
