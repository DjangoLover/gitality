from celery import task


@task
def inspect_achievement(achievements, entity_type, entity, dirty_fields):
    """
    Background celery task for achievements inspection.
    """

    # Getting only achievements that have sense to be checked
    achievements = achievements.filter(
        entity_type=entity_type,
        requirements__key__in=dirty_fields.keys()
    # NOTE: Excluding unlocked achievements
    ).exclude(
        id__in=entity.achievements.values_list('achievement_id', flat=True)
    ).distinct()

    # Inspecting
    for achievement in achievements:
        achievement.logic.inspect(entity)
