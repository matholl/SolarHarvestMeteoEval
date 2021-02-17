import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate


def import_guenhan(interp_range):


    print('Loading skin\'s transmission factor')

    #keeping bashkatov naming for main.py and other modules
    bashkatov = {}


    df = pd.read_csv('./data_import/data/SkinTransmission_Guenhan.csv')

    wavelength = df.lambdaNM
    depth = df.implantdepthCM
    skinTransm = df.SkinTransm

    depth25mm = df['implantdepthCM']==2.5

    # print(df[depth25mm].lambdaNM)
    # print(df[depth25mm].SkinTransm)
    bashkatov['wavelengths'] = df[depth25mm].lambdaNM
    bashkatov['tf'] = df[depth25mm].SkinTransm

    # Interpolate bashkatov
    f = interpolate.interp1d(bashkatov['wavelengths'], bashkatov['tf'], kind='linear')
    bashkatov['wavelength_interp'] = interp_range
    bashkatov['tf_interp'] = f(bashkatov['wavelength_interp'])


    # plt.figure()
    # plt.plot(bashkatov['wavelengths'], bashkatov['tf'], 'b', label = 'data')
    # plt.plot(bashkatov['wavelength_interp'], bashkatov['tf_interp'], '--r', label = 'interp')
    # plt.xlabel('wavelength [nm]')
    # plt.ylabel('TF []')
    # plt.legend()
    # plt.show()

    return bashkatov

def get_bashkatov(interp_range):
    print('Loading skin\'s transmission factor')
    bashkatov = {}

    path = './data_import/data/PenetrationDepth_Bashkatov.csv'
    f = open(path)
    reader = csv.reader(f, delimiter = ',')
    df = list(reader)
    f.close()

    # lambda
    bashkatov['wavelengths'] = [item[0] for item in df]
    del bashkatov['wavelengths'][0]
    bashkatov['wavelengths'] = [float(bashkatov['wavelengths'][p]) for p in range(0,len(bashkatov['wavelengths']))]

    # penetration depth
    bashkatov['pen_depth'] = [item[1] for item in df]
    del bashkatov['pen_depth'][0]
    bashkatov['pen_depth'] = [float(bashkatov['pen_depth'][p]) for p in range(0,len(bashkatov['pen_depth']))]

    del df

    bashkatov['skin_thickness'] = 2.5

    bashkatov['tf'] = []
    for i in range(0, len(bashkatov['pen_depth'])):
        if bashkatov['pen_depth'][i] == 0:
            bashkatov['tf'].append(0)
        else:
            bashkatov['tf'].append(np.exp(-(bashkatov['skin_thickness']/bashkatov['pen_depth'][i]))) # skin thickness and penetration depth are both in mm

    # Interpolate bashkatov
    f = interpolate.interp1d(bashkatov['wavelengths'], bashkatov['tf'], kind='linear')
    bashkatov['wavelength_interp'] = interp_range
    bashkatov['tf_interp'] = f(bashkatov['wavelength_interp'])

    return bashkatov


def main():
    bashkatov = import_guenhan()

    return

if __name__ == '__main__':
    main()
