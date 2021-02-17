#%%
import os
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature

#%% plot estimated power output from get_artificial_user_profiles.py
def plot_estimated_power(data, station_ids, months, year_of_interest, user_name, plot_path, i):
    #%%
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    # generate figure
    filename = str(year_of_interest) + '_' + str(data[station_ids[i]]['station_name'].replace(" ", "")) + '_' + 'estimated_power.pdf'
    pdffile = plot_path + filename

    # get list of all available months for the current station
    months = list(data[station_ids[i]]['month'].keys())
    # get int values of the months names
    months_int = [int(months[j]) for j in range(0,len(months))]
    # sort the int values for increasing numbers
    months_int.sort()
    # get sorted list of strings with numbers of months_int
    months = [str(x) for x in months_int]

    user_estpow_monthly_collector = {}
    for j in range(0, len(months)):
        for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
            user_estpow_monthly_collector['user_'+str(m)] = []


    for j in range(0, len(months)):
        for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
            user_estpow_monthly_collector['user_'+str(m)].append(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'][m])

    fig = plt.figure(figsize=(14, 14))
    for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
        if len(months) == 1:
            plt.plot(int(months[0]), user_estpow_monthly_collector['user_'+str(m)], 'o')
        else:
            plt.plot(months_int, user_estpow_monthly_collector['user_'+str(m)], '*-')
    plt.plot(months_int, [1e-5]*len(months), '--r')
    plt.xlim([min([int(months[q]) for q in range(0, len(months))]), max([int(months[q]) for q in range(0, len(months))])])
    plt.xlabel('Month of current year')
    plt.gca().set_ylim(bottom=0)
    plt.ylabel(r'Estimated mean power output (TF = .2, EQE = .2, A = 3.6 $cm^2$) [W]')
    plt.grid('on')
    plt.xticks([int(months[q]) for q in range(0, len(months))])

    # check data quality and addidional information and add it below the plot
    figure_text = 'Additional Information: \n'
    bad_glo_count = 0
    for j in range(0, len(months)):
        if data[station_ids[i]]['month'][months[j]]['glo_NANs'] > .5 * len(data[station_ids[i]]['month'][months[j]]['glo']):
            bad_glo_count += 1
            if bad_glo_count == 1:
                figure_text += 'Substantial (>.5) data missing for months: ' + months[j]
            else:
                figure_text += ', ' + months[j]
                bad_glo_count += 1
    if bad_glo_count > 0:
        figure_text += '\nMean power output user- and months-specific:\n'
    else:
        figure_text += 'Mean power output user- and months-specific:\n'

    fig.subplots_adjust(bottom=0.35)

    for m in range(0, len(data[station_ids[i]]['month'][months[j]]['mean_power_estimate'])):
        figure_text += user_name[m] + ' : '
        for j in range(0, len(months)):
            if j < len(months) - 1:
                if j % 4 == 0 and j != 0:
                    figure_text += ' mean-p (' + months[j] + ') = ' + ' %.2E' % user_estpow_monthly_collector['user_'+str(m)][j] + ' W,\n'
                else:
                    figure_text += ' mean-p (' + months[j] + ') = ' + ' %.2E' % user_estpow_monthly_collector['user_'+str(m)][j] + ' W, '
            else:
                figure_text += ' mean-p (' + months[j] + ') = ' + ' %.2E' % user_estpow_monthly_collector['user_'+str(m)][j] + ' W,'
        figure_text += ' Yearly mean-p = ' + ' %.2E' % data[station_ids[i]]['yearly']['mean_power_estimate'][str(m)] + ' W.\n'

    plt.figtext(.08, .02, figure_text)
    plt.title(data[station_ids[i]]['station_name'] + ' ' + str(year_of_interest))
    plt.legend(user_name + ['10 uW'])
    plt.savefig(pdffile)
    plt.close()

    #%%
    return

#%% plot isc power output from power_output.py
def plot_isc_power(data, station_ids, months, year_of_interest, user_name, plot_path, i):
    #%%
    if not os.path.exists(plot_path):
        os.makedirs(plot_path)

    # generate figure
    filename = str(year_of_interest) + '_' + str(data[station_ids[i]]['station_name'].replace(" ", "")) + '_' + 'isc_power.pdf'
    pdffile = plot_path + filename

    # get list of all available months for the current station
    months = list(data[station_ids[i]]['month'].keys())
    # get int values of the months names
    months_int = [int(months[j]) for j in range(0,len(months))]
    # sort the int values for increasing numbers
    months_int.sort()
    # get sorted list of strings with numbers of months_int
    months = [str(x) for x in months_int]

    user_isc_monthly_collector = {}
    for j in range(0, len(months)):
        for m in range(0, len(user_name)):
            user_isc_monthly_collector['user_'+str(m)] = []

    maxpower = 0
    minpower = 0
    for j in range(0, len(months)):
        for m in range(0, len(user_name)):
            if m != 7:
                user_isc_monthly_collector['user_'+str(m)].append(np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)]))
                if np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)]) > maxpower:
                    maxpower = np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)])
            if m == 7:
                user_isc_monthly_collector['user_'+str(m)].append(np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(2)]) + (13/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(5)]) + (91/104) *  np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(6)]))


    fig = plt.figure(figsize=(14, 14))
    for m in range(0, len(user_name)):
        if len(months) == 1:
            plt.plot(int(months[0]), user_isc_monthly_collector['user_'+str(m)], 'o')
        else:
            plt.plot(months_int, user_isc_monthly_collector['user_'+str(m)], '*-')
    plt.plot(months_int, [1e-5]*len(months))
    plt.xlim([min([int(months[q]) for q in range(0, len(months))]), max([int(months[q]) for q in range(0, len(months))])])
    plt.xlabel('Month of current year')
    plt.gca().set_ylim(bottom=0)
    plt.ylabel(r'Mean power output (isc-based) [W]')
    plt.ylim([minpower, maxpower*1.1])
    plt.grid('on')
    plt.xticks([int(months[q]) for q in range(0, len(months))])


    # calculate yearly mean power for publicaiton_user
    data[station_ids[i]]['yearly']['mean_power_isc'][str(m)] = data[station_ids[i]]['yearly']['mean_power_isc'][str(2)] + (13/104) * data[station_ids[i]]['yearly']['mean_power_isc'][str(5)] + (91/104) * data[station_ids[i]]['yearly']['mean_power_isc'][str(6)]

    # check data quality and addidional information and add it below the plot
    figure_text = 'Additional Information: \n'
    bad_glo_count = 0
    for j in range(0, len(months)):
        if data[station_ids[i]]['month'][months[j]]['glo_NANs'] > .5 * len(data[station_ids[i]]['month'][months[j]]['glo']):
            bad_glo_count += 1
            if bad_glo_count == 1:
                figure_text += 'Substantial (>.5) data missing for months: ' + months[j]
            else:
                figure_text += ', ' + months[j]
                bad_glo_count += 1
    if bad_glo_count > 0:
        figure_text += '\nMean power output user- and months-specific:\n'
    else:
        figure_text += 'Mean power output user- and months-specific:\n'

    fig.subplots_adjust(bottom=0.35)

    for m in range(0, len(user_name)):
        figure_text += user_name[m] + ' : '
        for j in range(0, len(months)):
            if j < len(months) - 1:
                if j % 4 == 0 and j != 0:
                    figure_text += ' mean-p (' + months[j] + ') = ' + ' %.2E' % user_isc_monthly_collector['user_'+str(m)][j] + ' W,\n'
                else:
                    figure_text += ' mean-p (' + months[j] + ') = ' + ' %.2E' % user_isc_monthly_collector['user_'+str(m)][j] + ' W, '
            else:
                figure_text += ' mean-p (' + months[j] + ') = ' + ' %.2E' % user_isc_monthly_collector['user_'+str(m)][j] + ' W,'
        figure_text += ' Yearly mean-p = ' + ' %.2E' % data[station_ids[i]]['yearly']['mean_power_isc'][str(m)] + ' W.\n'

    plt.figtext(.08, .02, figure_text)
    plt.title(data[station_ids[i]]['station_name'] + ' ' + str(year_of_interest))
    plt.legend(user_name + ['10 uW'])
    plt.savefig(pdffile)
    plt.close()

    #%%
    return

#%%
def collect_data_for_world_map(data, station_ids, months, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly):

    #%%
    for m in range(0, 7):
        lons[user_name[m]].append(data[station_ids[i]]['lon'])
        lats[user_name[m]].append(data[station_ids[i]]['lat'])
        for n in range(0, len(lats[user_name[m]])):
            if lats[user_name[m]][n] < -87:
               lats[user_name[m]][n] = -87
        labels_monthly[user_name[m]].append([' %.2E' % np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)]) for j in range(0, len(data[station_ids[i]]['month'].keys()))])
        # labels[user_name[m]].append(' %.2E' % data[station_ids[i]]['yearly']['mean_power_isc'][str(m)])
        labels[user_name[m]].append(' %.2E' % np.nanmean([np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(m)]) for j in range(0, len(data[station_ids[i]]['month'].keys()))]))

    ### Publication user: based on office worker with external lunch but no free time (m=2), 13/104 active weekend days (m=5, 1 active day per month) and 91/104 passive weekend days (m=6)

    if user_name[-1] != 'publicaiton_user':
        user_name.append('publicaiton_user')
        m = len(user_name)-1
        lons[user_name[m]] = []
        lats[user_name[m]] = []
        labels[user_name[m]] = []
        labels_monthly[user_name[m]] = []
    m = len(user_name)-1


    lons[user_name[m]].append(data[station_ids[i]]['lon'])
    lats[user_name[m]].append(data[station_ids[i]]['lat'])
    for n in range(0, len(lats[user_name[m]])):
        if lats[user_name[m]][n] < -87:
           lats[user_name[m]][n] = -87

    ### Publication user: based on office worker with external lunch but no free time (m=2), 13/104 active weekend days (m=5, 1 active day per month) and 91/104 passive weekend days (m=6)
    calc_year_1 = np.nanmean([np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(2)]) \
                                + (13/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(5)]) \
                                + (91/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(6)]) \
                                for j in range(0, len(data[station_ids[i]]['month'].keys()))])
    labels[user_name[m]].append(' %.2E' % calc_year_1)
    labels_monthly[user_name[m]].append([' %.2E' % (np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(2)]) + (13/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(5)]) + (91/104) * np.nanmean(data[station_ids[i]]['month'][months[j]]['p_calc'][str(6)])) for j in range(0, len(data[station_ids[i]]['month'].keys()))])


    #%%
    return lons, lats, labels, labels_monthly


#%% plot isc power output on world map
def plot_isc_power_on_world_map_circle_method(data, station_ids, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly):
    #%%
    c_m = []
    for m in range(0, len(user_name)):

        # filename
        if not os.path.exists(plot_path):
            os.makedirs(plot_path + 'world_map/')
        filename = str(year_of_interest) + '_' + 'isc_power_world_map_circles_user_' + str(m) + '.pdf'
        pdffile = plot_path + 'world_map/' + filename

        # circle radii
        r_main = 1
        r_sub = .5

        # figure
        plt.figure(figsize=(20, 10))
        ax1 = plt.axes(projection=ccrs.PlateCarree())
        ax1.coastlines()
        ax1.add_feature(cfeature.RIVERS)
        ax1.add_feature(cfeature.LAKES)
        ax1.add_feature(cfeature.COASTLINE)
        ax1.add_feature(cfeature.BORDERS)
        ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
        ax1.stock_img()

        # yearly labels
        labels_yearly = [float(labels[user_name[m]][p]) for p in range(0, len(labels[user_name[m]]))]
        c = []
        for q in range(0, len(labels[user_name[m]])):
            if labels_yearly[q] < 1e-5:
                c.append('r')
            else:
                c.append('g')
        for g in range(0, len(lons[user_name[m]])):
            circ=plt.Circle((lons[user_name[m]][g], lats[user_name[m]][g]), radius=r_main, color=c[g],  zorder=2)
            ax1.add_patch(circ)

        # monthly labels

        # positioning helper
        d = r_sub + r_sub + 3 * r_sub # distance to center of main point in °
        alpha = 1/12 * 2 * np.pi
        d_y = []
        d_x = []
        d_x_a = []
        d_y_a = []
        for q in range(0, 12):
            d_y.append(d * np.cos(alpha * q))
            d_x.append(d * np.sin(alpha * q))
            d_x_a.append(d * 1.3 * np.sin(alpha * q))
            d_y_a.append(d * 1.3 * np.cos(alpha * q))

        # color of dot
        c_m_collector1 = []
        for q in range(0, len(labels_monthly[user_name[m]])):
            c_m_collector2 = []
            for n in range(0, len(labels_monthly[user_name[m]][q])):
                if float(labels_monthly[user_name[m]][q][n]) < 1e-5:
                    c_m_collector2.append('r')
                else:
                    c_m_collector2.append('g')
            c_m_collector1.append(c_m_collector2)
        c_m.append(c_m_collector1)

        # plots
        for q in range(0, len(labels_monthly[user_name[m]])): # stations
            for n in range(0, len(labels_monthly[user_name[m]][q])): # months
                circ=plt.Circle((lons[user_name[m]][q] + d_x[n],lats[user_name[m]][q] + d_y[n]), radius=r_sub, color=c_m[m][q][n],  zorder=2)
                ax1.add_patch(circ)

        plt.title('Mean power output of user ' + user_name[m] + ' in ' + str(year_of_interest) + ' red if sub 10 uW', fontsize = 14, y = 1.03)
        plt.tight_layout()
        # plt.show()
        plt.savefig(pdffile, dpi = 300)
        plt.close()

    #%%
    return




#%% plot isc power output on world map
def plot_isc_power_on_world_map_circle_method_publication(data, station_ids, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly):
    #%%

    # new user based on user 2 (office worker, external lunch, no free time + 13/104 weekend days active (m=5), 91/104 weekend days inactive (m=6))
    c_m = []
    m=7


    # print(lons)
    # print(lats)
    # print(labels)
    # print(labels_monthly)


    # filename
    if not os.path.exists(plot_path):
        os.makedirs(plot_path + 'world_map/')
    filename = str(year_of_interest) + '_' + 'isc_power_world_map_circles_user_' + str(m) + '_publication.pdf'
    pdffile = plot_path + 'world_map/' + filename

    # circle radii
    r_main = 1
    r_sub = .5

    # figure
    plt.figure(figsize=(20, 10))
    ax1 = plt.axes(projection=ccrs.PlateCarree())
    ax1.coastlines()
    ax1.add_feature(cfeature.RIVERS)
    ax1.add_feature(cfeature.LAKES)
    ax1.add_feature(cfeature.COASTLINE)
    ax1.add_feature(cfeature.BORDERS)
    ax1.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='--')
    ax1.stock_img()

    # yearly labels
    labels_yearly = [float(labels[user_name[m]][p]) for p in range(0, len(labels[user_name[m]]))]
    c = []
    for q in range(0, len(labels[user_name[m]])):
        if labels_yearly[q] < 1e-5:
            c.append('r')
        else:
            c.append('g')
    for g in range(0, len(lons[user_name[m]])):
        circ=plt.Circle((lons[user_name[m]][g], lats[user_name[m]][g]), radius=r_main, color=c[g],  zorder=2)
        ax1.add_patch(circ)

    # monthly labels

    # positioning helper
    d = r_sub + r_sub + 3 * r_sub # distance to center of main point in °
    alpha = 1/12 * 2 * np.pi
    d_y = []
    d_x = []
    d_x_a = []
    d_y_a = []
    for q in range(0, 12):
        d_y.append(d * np.cos(alpha * q))
        d_x.append(d * np.sin(alpha * q))
        d_x_a.append(d * 1.3 * np.sin(alpha * q))
        d_y_a.append(d * 1.3 * np.cos(alpha * q))

    # color of dot
    c_m_collector1 = []
    for q in range(0, len(labels_monthly[user_name[m]])):
        c_m_collector2 = []
        for n in range(0, len(labels_monthly[user_name[m]][q])):
            if float(labels_monthly[user_name[m]][q][n]) < 1e-5:
                c_m_collector2.append('r')
            else:
                c_m_collector2.append('g')
        c_m_collector1.append(c_m_collector2)
    c_m.append(c_m_collector1)


    # plots
    for q in range(0, len(labels_monthly[user_name[m]])): # stations
        for n in range(0, len(labels_monthly[user_name[m]][q])): # months

            # print('m: ' + str(m))
            # print('n: ' + str(n))
            # print('q: ' + str(q))

            circ=plt.Circle((lons[user_name[m]][q] + d_x[n],lats[user_name[m]][q] + d_y[n]), radius=r_sub, color=c_m[0][q][n],  zorder=2)
            ax1.add_patch(circ)

    plt.title('Mean power output of user ' + user_name[m] + ' in ' + str(year_of_interest) + ' red if sub 10 uW', fontsize = 14, y = 1.03)
    plt.tight_layout()
    # plt.show()
    plt.savefig(pdffile, dpi = 300)
    plt.close()

    #%%
    return




def world_map_legend(data, station_ids, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly):
    #%%
    # filename
    if not os.path.exists(plot_path):
        os.makedirs(plot_path + 'world_map/')
    filename = str(year_of_interest) + '_' + 'world_map_legend.pdf'
    pdffile = plot_path + 'world_map/' + filename

    #%%
    # positioning helper
    d = 150 # distance to center of main point in °
    alpha = 1/12 * 2 * np.pi
    d_y = []
    d_x = []
    d_x_a = []
    d_y_a = []
    for q in range(0, 12):
        d_y.append(d * np.cos(alpha * q))
        d_x.append(d * np.sin(alpha * q))
        d_x_a.append(d * 1.3 * np.sin(alpha * q))
        d_y_a.append(d * 1.3 * np.cos(alpha * q))

    # main circle
    fig=plt.figure()
    axis_cutoff = 300
    plt.axis([-axis_cutoff,axis_cutoff,-axis_cutoff,axis_cutoff])
    ax=fig.add_subplot(1,1,1)
    circ=plt.Circle((0,0), radius=100, color='k', fill=False)
    ax.add_patch(circ)

    for n in range(0, 12): # months
        circ=plt.Circle((d_x[n],d_y[n]), radius=25, color='k', fill=False)
        ax.add_patch(circ)


    plt.axis('equal')
    plt.axis('off')

    for n in range(0, 12):
        plt.annotate(str(n+1),  xy=(d_x[n]-6, d_y[n]-6))
    plt.annotate('monthly values',  xy=(d_x_a[0], d_y_a[0]+0.01))
    plt.annotate('mean power',  xy=(-45, 15))
    plt.annotate('whole year',  xy=(-45, -5))
    plt.annotate('red if < 10 uW',  xy=(-45, -25))

    #%%
    plt.tight_layout()
    # plt.show()
    plt.savefig(pdffile)
    plt.close()

    #%%
    return







































#%%
#%%

###############################################################################
###############################################################################
###############################################################################
############################ Old functions ####################################
###############################################################################
###############################################################################
###############################################################################

#%%
#%%


##%% plot isc power output on world map
#def plot_isc_power_on_world_map(data, station_ids, year_of_interest, user_name, plot_path, i, lons, lats, labels, labels_monthly):
#    #%%
#    c_m = []
#    for m in range(0, len(user_name)):
#
#        # filename
#        if not os.path.exists(plot_path):
#            os.makedirs(plot_path)
#        filename = str(year_of_interest) + '_' + 'isc_power_world_map_user_' + str(m) + '.pdf'
#        pdffile = plot_path + filename
#
#        # figure
#        plt.figure(figsize=(20, 10))
#        ax1 = plt.axes(projection=ccrs.PlateCarree())
#        ax1.coastlines()
#        ax1.add_feature(cfeature.RIVERS)
#        ax1.add_feature(cfeature.LAKES)
#        ax1.add_feature(cfeature.COASTLINE)
#        ax1.add_feature(cfeature.BORDERS)
#        ax1.stock_img()
#
#        # yearly labels
#        labels_yearly = [float(labels[user_name[m]][p]) for p in range(0, len(labels[user_name[m]]))]
#        c = []
#        for q in range(0, len(labels[user_name[m]])):
#            if labels_yearly[q] < 1e-5:
#                c.append('r')
#            else:
#                c.append('g')
#        ax1.scatter(lons[user_name[m]], lats[user_name[m]], marker='o', edgecolor = 'black',  c=c,  s=100,  zorder=2)
#
#        # monthly labels
#
#        # positioning helper
#        d = 3 # distance to center of main point in °
#        alpha = 1/12 * 2 * np.pi
#        d_y = []
#        d_x = []
#        for q in range(0, 12):
#            d_y.append(d * np.cos(alpha * q))
#            d_x.append(d * np.sin(alpha * q))
#
#        # color of dot
#        c_m_collector1 = []
#        for q in range(0, len(labels_monthly[user_name[m]])):
#            c_m_collector2 = []
#            for n in range(0, len(labels_monthly[user_name[m]][q])):
#                if float(labels_monthly[user_name[m]][q][n]) < 1e-5:
#                    c_m_collector2.append('r')
#                else:
#                    c_m_collector2.append('g')
#            c_m_collector1.append(c_m_collector2)
#        c_m.append(c_m_collector1)
#
#        # plots
#        for q in range(0, len(labels_monthly[user_name[m]])): # stations
#            for n in range(0, len(labels_monthly[user_name[m]][q])): # months
#                ax1.scatter(lons[user_name[m]][q] + d_x[n], lats[user_name[m]][q] + d_y[n], marker='o', edgecolor = 'k',  c=c_m[m][q][n],  s=20,  zorder=2)
#
#        plt.title('Mean power output of user ' + user_name[m] + ' in ' + str(year_of_interest) + ' red if sub 10 uW', fontsize = 14, y = 1.02)
#        plt.tight_layout()
#        plt.savefig(pdffile, dpi = 300)
#        plt.show()
#        plt.close()
#
#    #%%
#    return
