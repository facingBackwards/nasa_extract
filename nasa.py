#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from collections import namedtuple
from collections import defaultdict
import enum

class RecordType(enum.Enum):
    SUMMARY = 1
    COLD_REFERENCE = 2
    WARM_REFERENCE = 3
    AVERAGE_RESPONSIVITY = 4
    NOISE_EQUIVALENT_RADIANCE = 5
    AVERAGE_INSTRUMENT_TEMP = 6
    SD_INSTRUMENT_TEMP = 7
    CALIBRATED_ATMOSPHERIC_SPECTRUM = 8


Summary = namedtuple('Summary', (
    'satellite_id '
    'initial_wave_number '
    'final_wave_number '
    'wave_number_increment '
    'start_orbit '
    'end_orbit '
    'mean_bolometer_temp '
    'sd_bolometer_temp '
    'mean_bb_temp '
    'sd_bb_temp '
    'mean_bs_temp '
    'sd_bs_temp '
    'mean_mdm_temp '
    'sd_mdm_temp '
    'mean_imcc_temp '
    'sd_imcc_temp '
    'mean_cs_temp '
    'sd_cs_temp '
    'rcs_count '
    'orbit_count '
    'orbits'))
ColdReference = namedtuple('ColdReference', (
    'start_orbit '
    'end_orbit '
    'spectra_count '
    'avg_peak_value '
    'sd_peak_value '
    'avg_peak_position '
    'sd_peak_position '
    'avg_cr_spectrum_intensity'))
WarmReference = namedtuple('WarmReference', (
    'start_orbit '
    'end_orbit '
    'spectra_count '
    'avg_peak_value '
    'sd_peak_value '
    'avg_peak_position '
    'sd_peak_position '
    'avg_wr_spectrum_intensity'))
AverageResponsivity = namedtuple('AverageResponsivity', (
    'start_orbit '
    'end_orbit '
    'avg_responsivity'))
NoiseEquivalentRadiance = namedtuple('NoiseEquivalentRadiance', (
    'start_orbit '
    'end_orbit '
    'ner'))
AverageInstrumentTemp = namedtuple('AverageInstrumentTemp', (
    'start_orbit '
    'end_orbit '
    'avg_instrument_temp'))
SDInstrumentTemp = namedtuple('SDInstrumentTemp', (
    'start_orbit '
    'end_orbit '
    'sd_instrument_temp'))
CalibratedAtmosphericSpectrum = namedtuple('CalibratedAtmosphericSpectrum', (
    'orbit_number '
    'spectrum_number '
    'day '
    'hour '
    'minute '
    'second '
    'latitude '
    'longitude '
    'height '
    'solar_elevation_angle '
    'bolo_temp '
    'blackbody_temp '
    'blackbody_temp_redundant '
    'beamsplitter_temp '
    'mmmd_temp '
    'imcc_temp '
    'cs_temp '
    'imcc_position '
    'positive_volt_cal '
    'zero_volt_cal '
    'negative_volt_cal '
    'cal_transducer '
    'bit_error_count '
    'gain_pulses_outside_center '
    'time_indicator '
    'specific_intensity'))

def orbit_times(*dat):
    return tuple(int_(i) for i in dat[:4]), tuple(int_(i) for i in dat[4:])

def make_summary(r):
    r.insert(0, [])
    lower, upper = o_range(r[6])
    orbits = [orbit_times(*r[i:i+8]) for i in range(26, 170, 8)]
    record = Summary(
            satellite_id=int_(r[2]),
            initial_wave_number=ibm360(r[3]),
            final_wave_number=ibm360(r[4]),
            wave_number_increment=ibm360(r[5]),
            start_orbit=lower,
            end_orbit=upper,
            mean_bolometer_temp=ibm360(r[8]),
            sd_bolometer_temp=ibm360(r[9]),
            mean_bb_temp=ibm360(r[10]),
            sd_bb_temp=ibm360(r[11]),
            mean_bs_temp=ibm360(r[12]),
            sd_bs_temp=ibm360(r[13]),
            mean_mdm_temp=ibm360(r[14]),
            sd_mdm_temp=ibm360(r[15]),
            mean_imcc_temp=ibm360(r[16]),
            sd_imcc_temp=ibm360(r[17]),
            mean_cs_temp=ibm360(r[18]),
            sd_cs_temp=ibm360(r[19]),
            rcs_count=ibm360(r[23]),
            orbit_count=int_(r[25]),
            orbits=orbits
            )
    return record

def make_cold(r):
    r.insert(0, [])
    start, end = o_range(r[2])
    record = ColdReference(
            start_orbit=start,
            end_orbit=end,
            spectra_count=int_(r[3]),
            avg_peak_value=ibm360(r[4]),
            sd_peak_value=ibm360(r[5]),
            avg_peak_position=ibm360(r[6]),
            sd_peak_position=ibm360(r[7]),
            avg_cr_spectrum_intensity=[ibm360(i) for i in r[30:]]
            )
    return record

def make_warm(r):
    r.insert(0, [])
    start, end = o_range(r[2])
    record = WarmReference(
            start_orbit=start,
            end_orbit=end,
            spectra_count=int_(r[3]),
            avg_peak_value=ibm360(r[4]),
            sd_peak_value=ibm360(r[5]),
            avg_peak_position=ibm360(r[6]),
            sd_peak_position=ibm360(r[7]),
            avg_wr_spectrum_intensity=[ibm360(i) for i in r[30:]]
            )
    return record

def make_responsivity(r):
    r.insert(0,[])
    start, end = o_range(r[2])
    record = AverageResponsivity(
            start_orbit=start,
            end_orbit=end,
            avg_responsivity=[ibm360(i) for i in r[30:]]
            )
    return record

def make_ner(r):
    r.insert(0, [])
    start, end = o_range(r[2])
    record = NoiseEquivalentRadiance(
            start_orbit=start,
            end_orbit=end,
            ner=[ibm360(i) for i in r[30:]]
            )
    return record

def make_ait(r):
    r.insert(0, [])
    start, end = o_range(r[2])
    record = AverageInstrumentTemp(
            start_orbit=start,
            end_orbit=end,
            avg_instrument_temp=[ibm360(i) for i in r[30:]]
            )
    return record

def make_sd_of_it(r):
    r.insert(0, [])
    start, end = o_range(r[2])
    record = SDInstrumentTemp(
            start_orbit=start,
            end_orbit=end,
            sd_instrument_temp=[ibm360(i) for i in r[30:]]
            )
    return record

def make_cas(r):
    r.insert(0, [])
    record = CalibratedAtmosphericSpectrum(
            orbit_number=int_(r[2]),
            spectrum_number=int_(r[3]),
            day=int_(r[4]),
            hour=int_(r[5]),
            minute=int_(r[6]),
            second=int_(r[7]),
            latitude=int_(r[8]),
            longitude=int_(r[9]),
            height=ibm360(r[10]),
            solar_elevation_angle=ibm360(r[11]),
            bolo_temp=ibm360(r[12]),
            blackbody_temp=ibm360(r[13]),
            blackbody_temp_redundant=ibm360(r[14]),
            beamsplitter_temp=ibm360(r[15]),
            mmmd_temp=ibm360(r[16]),
            imcc_temp=ibm360(r[17]),
            cs_temp=ibm360(r[18]),
            imcc_position=int_(r[19]),
            positive_volt_cal=ibm360(r[20]),
            zero_volt_cal=ibm360(r[21]),
            negative_volt_cal=ibm360(r[22]),
            cal_transducer=ibm360(r[23]),
            bit_error_count=ibm360(r[26]),
            gain_pulses_outside_center=ibm360(r[27]),
            time_indicator=int_(r[28]),
            specific_intensity=[ibm360(i) for i in r[30:]]
            )
    return record

RECORD_TYPES = {RecordType.SUMMARY: make_summary,
        RecordType.COLD_REFERENCE: make_cold,
        RecordType.WARM_REFERENCE: make_warm,
        RecordType.AVERAGE_RESPONSIVITY: make_responsivity,
        RecordType.NOISE_EQUIVALENT_RADIANCE: make_ner,
        RecordType.AVERAGE_INSTRUMENT_TEMP: make_ait,
        RecordType.SD_INSTRUMENT_TEMP: make_sd_of_it,
        RecordType.CALIBRATED_ATMOSPHERIC_SPECTRUM: make_cas}
FRAME = 3572

def ibm360(dat):
    b = int.from_bytes(dat, byteorder='big')
    sign = b>>31
    ex = (b>>24)&127 -64
    frac = float.fromhex('.'+hex(b&((2<<23)-1))[2:])
    # print(sign, ex, frac)
    return (-sign or 1) * frac * 16**ex

def int_(dat):
    return int.from_bytes(dat, byteorder='big')

def o_range(dat):
    return int_(dat[:2]), int_(dat[2:])

def process_record(raw):
    if len(raw) != 891:
        raise ValueError(f'Invalid record length {len(raw)}')
    record_type = RecordType(int_(raw[0]))
    record = RECORD_TYPES[record_type](raw)

    return record_type, record

def process_file(file_path):
    with open(file_path, 'rb') as dat:
        frame = dat.read(FRAME)
        # click.echo(len(frame))
        while frame:
            data = [frame[i:i+4] for i in range(0,  893*4, 4)]
            # click.echo(data[:10])
            # click.echo(len(data))
            yield process_record(data[2:])
            frame = dat.read(FRAME)


@click.command()
@click.argument('data')
@click.option('--count')
def cli(data, count=10):
    records = defaultdict(list)
    for r_type, record in process_file(data):
        records[r_type.name].append(record)
    for r_type, records in records.items():
        print(r_type, len(records))
if __name__ == "__main__":
    cli()

