extends Control

var _letters: Dictionary[String, VoiceButton] = {}

var mic_player: AudioStreamPlayer

func _ready() -> void:
    for button in $VSplitContainer/ScrollContainer/VBoxContainer.get_children():
        if button is VoiceButton:
            _letters[button.text.to_lower()] = button

    mic_player = AudioStreamPlayer.new()
    mic_player.stream = AudioStreamMicrophone.new()
    mic_player.bus = "Record"
    add_child(mic_player)

    mic_player.play()

func _on_button_pressed() -> void:
    var text = $VSplitContainer/HBoxContainer/TextEdit.text
    for c: String in text:
        if c.to_lower() in _letters:
            _letters[c.to_lower()].play()
            await get_tree().create_timer($VSplitContainer/HBoxContainer/delay.value).timeout

func _on_pitch_value_changed(value: float) -> void:
    var effect: AudioEffectPitchShift = AudioServer.get_bus_effect(AudioServer.get_bus_index("output"), 0)
    effect.pitch_scale = value
