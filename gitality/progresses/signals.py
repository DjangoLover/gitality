from django.dispatch import Signal


# Signal that is sent whenever certain
# entity progress state is changed.
progress_state_changed = Signal(
    providing_args=[
        'entity_type',
        'entity',
        'dirty_fields'
    ]
)
