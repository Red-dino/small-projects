class_name VoiceButton
extends Button

var letter = ''

# We get the index of the "Record" bus.
var idx = AudioServer.get_bus_index("Record")
# And use it to retrieve its first effect, which has been defined
# as an "AudioEffectRecord" resource.
var effect: AudioEffectRecord = AudioServer.get_bus_effect(idx, 0)

var audio_stream_player: AudioStreamPlayer

var has_recording = false
var start_time: float = 0.0

func _ready() -> void:
    letter = text
    pressed.connect(_on_press)
    
    audio_stream_player = AudioStreamPlayer.new()
    audio_stream_player.bus = &"output"
    add_child(audio_stream_player)

func _on_press() -> void:
    if effect.is_recording_active():
        var recording = effect.get_recording()
        audio_stream_player.stream = recording
        audio_stream_player.play(start_time)
        effect.set_recording_active(false)
        text = letter + " (Recorded)"
        has_recording = true
    else:
        effect.set_recording_active(true)
        text = "Recording..."
    
func play() -> void:
    if has_recording:
        audio_stream_player.play(start_time)
