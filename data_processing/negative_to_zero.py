def set_negative_radiation_to_zero(data, station_ids, i, months):
    print('Checking for negtive radiation values due to inaccuracies in the measurement device calibration.')
    for j in range(0, len(months)):
            for q in range(0, len(data[station_ids[i]]['month'][months[j]]['glo'])):
                if -10 < data[station_ids[i]]['month'][months[j]]['glo'][q] < 0:
                    data[station_ids[i]]['month'][months[j]]['glo'][q] = 0
                elif data[station_ids[i]]['month'][months[j]]['glo'][q] < -10 and data[station_ids[i]]['month'][months[j]]['glo'][q] != -999.0 and data[station_ids[i]]['month'][months[j]]['glo'][q] != -99.0:
                    data[station_ids[i]]['month'][months[j]]['glo'][q] = 0
                    print('Global radiation value below -10 W/m2 for station id %s at month %s and index %d' % (station_ids[i], months[j], q))
            for q in range(0, len(data[station_ids[i]]['month'][months[j]]['dir'])):
                if -10 < data[station_ids[i]]['month'][months[j]]['dir'][q] < 0:
                    data[station_ids[i]]['month'][months[j]]['dir'][q] = 0
                elif data[station_ids[i]]['month'][months[j]]['dir'][q] < -10  and data[station_ids[i]]['month'][months[j]]['dir'][q] != -999.0 and data[station_ids[i]]['month'][months[j]]['dir'][q] != -99.0:
                    data[station_ids[i]]['month'][months[j]]['dir'][q] = 0
                    print('Direct radiation value below -10 W/m2 for station id %s at month %s and index %d' % (station_ids[i], months[j], q))
            for q in range(0, len(data[station_ids[i]]['month'][months[j]]['dif'])):
                if -10 < data[station_ids[i]]['month'][months[j]]['dif'][q] < 0:
                    data[station_ids[i]]['month'][months[j]]['dif'][q] = 0
                elif data[station_ids[i]]['month'][months[j]]['dif'][q] < -10  and data[station_ids[i]]['month'][months[j]]['dif'][q] != -999.0 and data[station_ids[i]]['month'][months[j]]['dif'][q] != -99.0:
                    data[station_ids[i]]['month'][months[j]]['dif'][q] = 0
                    print('Diffuse radiation value below -10 W/m2 for station id %s at month %s and index %d' % (station_ids[i], months[j], q))
    return data