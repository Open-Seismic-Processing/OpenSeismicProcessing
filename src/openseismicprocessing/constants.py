"""
Shared constant values used across the Open Seismic Processing package.

Currently acts as a placeholder for SEG-Y revision defaults; populate
`SEGY_REVISIONS` with your dictionaries when ready.
"""

BINARY_HEADER_REV0 = {
    # 1–12: job / line / reel IDs
    "job_id":                     (1, 4),   # Job identification number
    "line_number":                (5, 4),   # Line number (inline for 3D poststack)
    "reel_number":                (9, 4),   # Reel number

    # 13–16: traces per ensemble
    "data_traces_per_ensemble":   (13, 2),  # Number of data traces per ensemble
    "aux_traces_per_ensemble":    (15, 2),  # Number of auxiliary traces per ensemble

    # 17–24: dt / ns (current + original)
    "sample_interval":            (17, 2),  # dt (µs / Hz / m / ft)
    "sample_interval_original":   (19, 2),  # dt of original field recording
    "samples_per_trace":          (21, 2),  # ns
    "samples_per_trace_original": (23, 2),  # ns of original recording

    # 25–28: format and fold
    "data_sample_format":         (25, 2),  # format code (1=IBM, 5=IEEE, etc.)
    "ensemble_fold":              (27, 2),  # nominal fold per ensemble

    # 29–32: trace sorting & vertical sum
    "trace_sorting_code":         (29, 2),  # 1=as recorded, 2=CDP, 4=stacked, ...
    "vertical_sum_code":          (31, 2),  # 1=no sum, 2=two-sum, ...

    # 33–40: sweep definition
    "sweep_freq_start":           (33, 2),  # sweep start frequency
    "sweep_freq_end":             (35, 2),  # sweep end frequency
    "sweep_length_ms":            (37, 2),  # sweep length (ms)
    "sweep_type":                 (39, 2),  # 1=linear, 2=parabolic, 3=exp, 4=other

    # 41–48: sweep taper
    "sweep_channel_trace":        (41, 2),  # trace number of sweep channel
    "sweep_taper_start_ms":       (43, 2),  # sweep taper length at start (ms)
    "sweep_taper_end_ms":         (45, 2),  # sweep taper length at end (ms)
    "sweep_taper_type":           (47, 2),  # 1=linear, 2=cos², 3=other

    # 49–56: correlated / AGC / units
    "correlated_traces":          (49, 2),  # 1=no, 2=yes
    "binary_gain_recovered":      (51, 2),  # 1=yes, 2=no
    "amplitude_recovery_method":  (53, 2),  # 1=none, 2=divergence, 3=AGC, 4=other
    "measurement_system":         (55, 2),  # 1=meters, 2=feet

    # 57–60: polarity
    "impulse_polarity":           (57, 2),  # 1=upwards gives negative, 2=upwards gives positive
    "vibratory_polarity":         (59, 2),  # sweep phase / vibratory polarity code

    # 61–400: not defined in Rev-0 (vendor / user use)
    "unassigned_61_400":          (61, 400 - 60),  # 340 bytes
}

BINARY_HEADER_REV1 = {
    **BINARY_HEADER_REV0,
    # 301–302: SEG-Y format revision number (expects 0x0100 for Rev1)
    "segy_revision":              (301, 2),
    # 303–304: fixed-length trace flag (1=fixed, 0=variable)
    "fixed_length_trace_flag":    (303, 2),
    # 305–306: number of 3200-byte extended textual headers
    "extended_text_headers":      (305, 2),
    # 307–400: reserved/unused in Rev-1
    "unassigned_307_400":         (307, 400 - 306),
}

TRACE_HEADER_REV0 = {
    # 1–28: trace / ensemble IDs
    "tracl":   (1, 4),   # trace sequence number within line
    "tracr":   (5, 4),   # trace sequence number within file
    "fldr":    (9, 4),   # field record number
    "tracf":   (13, 4),  # trace number within field record
    "ep":      (17, 4),  # energy source point number
    "cdp":     (21, 4),  # ensemble (CDP / CMP / CRP / …)
    "cdpt":    (25, 4),  # trace number within ensemble

    # 29–36: type / stacking
    "trid":    (29, 2),  # trace identification code
    "nvs":     (31, 2),  # number of vertically summed traces
    "nhs":     (33, 2),  # number of horizontally stacked traces
    "duse":    (35, 2),  # data use (1=production, 2=test)

    # 37–68: offset + elevations / depths
    "offset":  (37, 4),  # source–receiver offset
    "gelev":   (41, 4),  # receiver elevation
    "selev":   (45, 4),  # source surface elevation
    "sdepth":  (49, 4),  # source depth below surface
    "gdel":    (53, 4),  # datum at receiver
    "sdel":    (57, 4),  # datum at source
    "swdep":   (61, 4),  # water depth at source
    "gwdep":   (65, 4),  # water depth at receiver

    "scalel":  (69, 2),  # scalar for elevations/depths (41–68)
    "scalco":  (71, 2),  # scalar for coordinates (73–88)

    # 73–88: source / receiver coordinates
    "sx":      (73, 4),  # source X
    "sy":      (77, 4),  # source Y
    "gx":      (81, 4),  # receiver X
    "gy":      (85, 4),  # receiver Y

    "counit":  (89, 2),  # coordinate units

    # 91–104: near-surface velocities & statics
    "wevel":   (91, 2),   # weathering velocity
    "swevel":  (93, 2),   # subweathering velocity
    "sut":     (95, 2),   # uphole time at source (ms)
    "gut":     (97, 2),   # uphole time at receiver (ms)
    "sstat":   (99, 2),   # source static correction (ms)
    "gstat":   (101, 2),  # receiver static correction (ms)
    "tstat":   (103, 2),  # total static applied (ms)

    # 105–114: lags, delay, mute
    "laga":    (105, 2),  # lag time A (ms)
    "lagb":    (107, 2),  # lag time B (ms)
    "delrt":   (109, 2),  # delay recording time (ms)
    "muts":    (111, 2),  # mute start time (ms)
    "mute":    (113, 2),  # mute end time (ms)

    # 115–118: ns / dt per trace
    "ns":      (115, 2),  # samples in this trace
    "dt":      (117, 2),  # sample interval (µs) for this trace

    # 119–126: gain & correlation
    "gain":    (119, 2),  # instrument gain type
    "igc":     (121, 2),  # gain constant (dB)
    "igi":     (123, 2),  # initial gain (dB)
    "corr":    (125, 2),  # 1=no, 2=yes (trace correlated)

    # 127–140: per-trace sweep info
    "sfs":     (127, 2),  # sweep frequency start (Hz)
    "sfe":     (129, 2),  # sweep frequency end (Hz)
    "slen":    (131, 2),  # sweep length (ms)
    "styp":    (133, 2),  # sweep type
    "stas":    (135, 2),  # sweep taper length at start (ms)
    "stae":    (137, 2),  # sweep taper length at end (ms)
    "tatyp":   (139, 2),  # taper type

    # 141–156: filters
    "afilf":   (141, 2),  # alias filter frequency (Hz)
    "afils":   (143, 2),  # alias filter slope
    "nofilf":  (145, 2),  # notch filter frequency (Hz)
    "nofils":  (147, 2),  # notch filter slope
    "lcf":     (149, 2),  # low cut frequency (Hz)
    "hcf":     (151, 2),  # high cut frequency (Hz)
    "lcs":     (153, 2),  # low cut slope
    "hcs":     (155, 2),  # high cut slope

    # 157–168: acquisition time / time basis
    "year":    (157, 2),  # year recorded
    "day":     (159, 2),  # day of year
    "hour":    (161, 2),
    "minute":  (163, 2),
    "sec":     (165, 2),
    "timbas":  (167, 2),  # time basis code

    # 169–180: group numbers / gaps
    "trwf":    (169, 2),  # trace weighting factor
    "grnors":  (171, 2),  # group number of roll-switch pos 1
    "grnofr":  (173, 2),  # group number of first trace in record
    "grnlof":  (175, 2),  # group number of last trace in record
    "gaps":    (177, 2),  # gap size
    "ofrav":   (179, 2),  # overtravel indicator

    # 181–240: *not* defined in SEG-Y Rev-0
    "unassigned_181_240": (181, 60),  # free / vendor-specific in 1975 spec
}

TRACE_HEADER_REV1 = {
    **TRACE_HEADER_REV0,
    # 181–188: transduction/measurement info
    "transduction_constant_mantissa": (181, 4),  # IEEE mantissa for trace values
    "transduction_constant_exponent": (185, 2),  # base-10 exponent for mantissa
    "transduction_units":             (187, 2),  # SEG-D code for measurement units

    # 189–192: timing and identification
    "time_scalar":                    (189, 2),  # scalar for all times in trace header
    "source_type_orientation":        (191, 2),  # source type/orientation code

    # 193–198: source energy direction vector
    "source_energy_dir_x":            (193, 2),
    "source_energy_dir_y":            (195, 2),
    "source_energy_dir_z":            (197, 2),

    # 199–206: source measurement (mantissa/exponent/unit)
    "source_measurement_mantissa":    (199, 4),
    "source_measurement_exponent":    (203, 2),
    "source_measurement_unit":        (205, 2),

    # 207–240: reserved/unused
    "unassigned_207_240":             (207, 240 - 206),
}
