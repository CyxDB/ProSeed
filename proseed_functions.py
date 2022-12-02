####################################
### Filename : proseed_functions.py
### Author   : Extav
### Date     : Nov 22 2022
####################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
import glob
import os
from matplotlib.patches import Rectangle
from matplotlib.patheffects import PathEffects

def get_eventid_from_slug(slug_string):
    
    return None

def getEventIDsFromOwner(o_id):

    query = """query getEventIDsFromOwner($ownerID : ID!) {
      tournaments(query: {
        page: 1,
        perPage: 500,
        filter: {
          ownerId: $ownerID
        }
      }) {
        nodes {
          name
          id
          events{
            id
          }
        }
      }
    }
    """

    variables = { "ownerID" : o_id}
    url = 'https://api.start.gg/gql/alpha'
    headers = {'Authorization': 'Bearer 9d5bfb54910992d8e3795039f1669237', 'Content-Type': 'application/json'}
    
    r = requests.post(url, headers=headers, json={'query': query, 'variables' : variables})
    assert r.status_code == 200, "status code should be 200"

    json_data = json.loads(r.text)
    tourney_list = json_data['data']['tournaments']['nodes']

    t_names = np.array([tourney['name'] for tourney in tourney_list if tourney['events']], dtype=str)
    e_ids = np.array([tourney['events'][0]['id'] for tourney in tourney_list if tourney['events']], dtype=int)

    colnames = ['t_name', 'e_id']
    dfdata = np.array([t_names, e_ids])
    dfdata = np.transpose(dfdata)
    new_df = pd.DataFrame(dfdata, columns=colnames)

    return new_df

def get_pIDs_and_pnames_from_eID(eID, bearer_token):
    """
    queries start.gg API using an event ID to return
    an array of player IDs and an array of the 
    corresponding player names
    """
    pID_array = np.array([])
    pname_array = np.array([])

    query = """query get_pnames_from_eid($e_id : ID!) {
        event(id : $e_id) {
        entrants (query : {
          page : 1,
          perPage : 500
        }) {
        nodes{
            participants{
                player{
                    gamerTag,
                    id
            }
            }
        }
        }
    }
    }"""

    variables = { "e_id" : eID}
    url = 'https://api.start.gg/gql/alpha'
    headers = {'Authorization': f'Bearer {bearer_token}', 'Content-Type': 'application/json'}

    r = requests.post(url, headers=headers, json={'query': query, 'variables' : variables})
    assert r.status_code == 200, "status code should be 200"

    json_data = json.loads(r.text)  

    entrants_list = json_data["data"]["event"]["entrants"]["nodes"]

    pID_array = np.array([entrant["participants"][0]["player"]["gamerTag"] for entrant in entrants_list], dtype=str)
    pname_array = np.array([entrant["participants"][0]["player"]["id"] for entrant in entrants_list], dtype=int)

    # return entrants_list
    return pID_array, pname_array

def getDataFromEventID(e_id):
    """
    queries start.gg API using an event ID
    to create a pandas dataFrame of relevant
    data from that event
    """
    #TO-DO include game_name and game_id to the query
    # test t_id : 489344
    query = """query getDataFromEventID($e_id:ID) {
        event(id : $e_id) {
        name,
        startAt,
    		tournament {
    		  id,
          name,
          slug,
          shortSlug,
    		},
        id,
        numEntrants,
        entrants(query: {
            page: 1,
            perPage: 500,
        }) {
            nodes {
            name,
            id,
            participants {
              player {
                id
              }
            }
            standing {
                placement
            } 
            }
        }
        }
        }
    """


    variables = { "e_id" : e_id}
    url = 'https://api.start.gg/gql/alpha'
    headers = {'Authorization': 'Bearer 9d5bfb54910992d8e3795039f1669237', 'Content-Type': 'application/json'}
    
    r = requests.post(url, headers=headers, json={'query': query, 'variables' : variables})
    assert r.status_code == 200, "status code should be 200"

    json_data = json.loads(r.text)
    # tourney_list = json_data['data']['tournaments']['nodes']
    # events_list = json_data['data']['tournaments']['nodes'][0]['events']
    # entrants_list = json_data['data']['tournaments']['nodes'][0]['events'][0]['entrants']['nodes']
    entrants_list = json_data['data']['event']['entrants']['nodes']
    tourney_data = json_data['data']['event']['tournament']


    # assertions that the tournament isn't empty
    # assert len(tourney_list) == 1, f'more than 1 tourney, bad id: {t_id}'
    # assert len(events_list) == 1, f'more than 1 event, bad id: {t_id}'
    assert len(entrants_list) > 0, f'more than 0 players, bad id: {e_id}'

    t_names = np.array([tourney_data['name'] for entrant in entrants_list if entrant['standing']], dtype=str)
    t_ids = np.array([tourney_data['id'] for entrant in entrants_list if entrant['standing']], dtype=int)
    t_starttimes = np.array([json_data['data']['event']['startAt'] for entrant in entrants_list if entrant['standing']], dtype=int)
    # t_s_slugs = np.array([tourney_list[0]['shortSlug'] for entrant in entrants_list if entrant['standing']], dtype=str)
    t_slugs = np.array([tourney_data['slug'] for entrant in entrants_list if entrant['standing']], dtype=str)
    # ev_names = np.array([events_list[0]['name'] for entrant in entrants_list if entrant['standing']], dtype=str)
    # ev_ids = np.array([events_list[0]['id'] for entrant in entrants_list if entrant['standing']], dtype=int)
    entrant_count = np.array([json_data['data']['event']['numEntrants'] for entrant in entrants_list if entrant['standing']], dtype=int)
    p_names = np.array([entrant['name'] for entrant in entrants_list if entrant['standing']], dtype=str)
    p_ids = np.array([entrant['participants'][0]['player']['id'] for entrant in entrants_list if entrant['standing']], dtype=int)
    standings = np.array([entrant['standing']['placement'] for entrant in entrants_list if entrant['standing']], dtype=int)

    # colnames = ['t_name', 't_id', 't_s_slug', 't_slug', 'ev_name', 'ev_id', 'entrants', 'p_name', 'p_id', 'standing']
    colnames = ['t_name','t_id', 't_starttime', 't_slug', 'entrant_count', 'p_name', 'p_id', 'p_standing']


    dfdata = np.array([t_names, t_ids, t_starttimes, t_slugs, entrant_count, p_names, p_ids, standings])
    dfdata = np.transpose(dfdata)
    new_df = pd.DataFrame(dfdata, columns=colnames)

    return new_df

def generate_text_dataframe_from_eventIDs(event_ID_array, savename="proseed_dataframe.csv"):
    # create the empty array
    colnames = ['t_name','t_id', 't_starttime', 't_slug', 'entrant_count', 'p_name', 'p_id', 'p_standing']
    df = pd.DataFrame([], columns=colnames)

    # run through each event and add to the df
    for e_id in event_ID_array:
        event_df = getDataFromEventID(e_id)
        df = pd.concat([df, event_df], ignore_index=True)

    df.to_csv(savename, index=False)
    return None

def generate_alltime_graph_from_pID(p1_or_p2, pID, df_filepath="proseed_dataframe.csv"):
    
    df = pd.read_csv(df_filepath)  
    
    ########## get the data for the player ##############################
    all_tourney_times = np.unique(df['t_starttime'].values)

    standings = np.array([], dtype=int)
    t_times = np.array([], dtype=float)
    entrant_counts = np.array([], dtype=int)

    for tourney_time in all_tourney_times:
        relevant_df = df[df['t_starttime'] == tourney_time]
        assert np.size(np.unique(relevant_df['entrant_count'].values)) == 1, 'same tourney diff entrant counts'
        entrant_count = relevant_df['entrant_count'].values[0]
        if len(relevant_df[relevant_df['p_id'] == pID]) > 0:
            standing = relevant_df[relevant_df['p_id'] == pID]['p_standing'].values[0]
        else:
            standing = -1

        standings = np.append(standings, standing)
        t_times = np.append(t_times, tourney_time)
        entrant_counts = np.append(entrant_counts, entrant_count)
    ########################################################################
    ############# create the plot ##########################################
    dpi = 150
    fig = plt.figure(dpi=dpi)
    ax1 = plt.subplot(111)
    px, py = fig.get_size_inches() * dpi  #pixel calculations

    #~~~~~~~~~~~ format size of graph ~~~~~~~~~~~~~~~~#
    xmin = np.min(t_times) - np.ptp(t_times) / np.size(t_times)
    xmax = np.max(t_times) + np.ptp(t_times) / np.size(t_times)
    ax1.set_xlim([xmin, xmax])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~ time/bar calculations ~~~~~~~~~~~~~~#
    week_in_seconds = 60 * 60 * 24 * 7
    time_offset = 12 * 60 * 60
    barwidth = week_in_seconds - time_offset
    barwidth_perc_of_img = barwidth / np.ptp([xmin, xmax]) 
    barwidth_in_pix = barwidth_perc_of_img * px
    markersize = barwidth_in_pix / 2
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~ plot the bars for tourneys entered ~~~~~~#
    truth_array = standings > 0    # has standings
    xvals = t_times[truth_array][::-1]
    yvals = entrant_counts[truth_array][::-1]


    bar_formatting = {
        'width' : barwidth,
        'color' : 'black',
    }
    ax1.bar(xvals, yvals, **bar_formatting)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~ plot the bars for tourneys NOT entered ~~~~~#
    truth_array = ~(standings > 0)   # no standings
    xvals = t_times[truth_array][::-1]
    yvals = entrant_counts[truth_array][::-1]

    bar_formatting = {
        'width' : barwidth,
        'color' : 'grey',
    }
    ax1.bar(xvals, yvals, **bar_formatting)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~ plot the placements ~~~~~~~~~~~~~~~#
    truth_array = (standings > 0)   # has standings
    xvals = t_times[truth_array][::-1]
    yvals = entrant_counts[truth_array][::-1] - standings[truth_array][::-1]
    plot_formatting = {
        'linestyle' : '-',
        'linewidth' : markersize / 20,
        'marker' : 'o',
        'ms' : markersize,
        'color' : 'red'
    }

    ax1.plot(xvals, yvals, **plot_formatting)
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~~~~~~ plot the text ~~~~~~~~~~~~~~~~~~#
    truth_array = (standings > 0)   # has standings
    for i,j,k in zip(xvals,standings[truth_array][::-1], yvals):
        ax1.annotate(str(j),     xy =(i, k), color='white',
                            fontsize=markersize/2, weight='heavy',
                            horizontalalignment='center',
                            verticalalignment='center_baseline')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~~~ final graph formatting ~~~~~~~~~~~~~~#
    ax1.set_xticks([])  # turn off x labels
    plt.title("Results over Time")   # plot title
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    plt.savefig(f"p{p1_or_p2}_alltime_graph.png")
    
    #########################################################################
    return None
    
def get_player_highest_placement(dF, p_id):
    """
    compares p_id to the dF to find out the best
    (lowest) placement. Returns -1 if no placement,
    but probably best not to send to this fn if
    no placement exists
    """
    player_dF = dF[dF['p_id'] == p_id]
    if len(player_dF) > 0:
        highest_placement = np.min(player_dF['p_standing'].values)
    else:
        highest_placement = -1

    return highest_placement

def get_player_number_bans(dF, p_id):
    player_dF = dF[dF['p_id'] == p_id]
    return len(player_dF)

def make_recent_tourney_bar_graph(df, p_id, savename):
    """
    DECEPTIVE NAME - Makes the graph for the statscreen,
    aka a fullsize graph with lots of detail meant to
    take up a significant portion of the screen

    Sort of a hot mess, and inefficient. Should be
    remade sometime (12/2/2022)
    """
    standings = df[df['p_id'] == p_id]['p_standing'].values.astype(int)
    t_names = df[df['p_id'] == p_id]['t_name'].values.astype(str)
    t_times = df[df['p_id'] == p_id]['t_starttime'].values.astype(int)
    # t_times = np.arange(len(t_times))
    entrant_counts = df[df['p_id'] == p_id]['entrant_count'].values.astype(int)

    ############## fill arrays for tourneys attended, tourneys not attended, etc #########
    ######################################################################################
    # region
    all_tourney_times = np.unique(df['t_starttime'].values)

    standings = np.array([], dtype=int)
    t_times = np.array([], dtype=int)
    entrant_counts = np.array([], dtype=int)

    for tourney_time in all_tourney_times:
        # is_right_tourney = df['t_starttime'] == tourney_time
        # has_player = df['p_id'] == p_id
        relevant_df = df[df['t_starttime'] == tourney_time]
        assert np.size(np.unique(relevant_df['entrant_count'].values)) == 1, 'same tourney diff entrant counts'
        entrant_count = relevant_df['entrant_count'].values[0]
        if len(relevant_df[relevant_df['p_id'] == p_id]) > 0:
            standing = relevant_df[relevant_df['p_id'] == p_id]['p_standing'].values[0]
        else:
            standing = -1

        standings = np.append(standings, standing)
        t_times = np.append(t_times, tourney_time)
        entrant_counts = np.append(entrant_counts, entrant_count)
    # endregion
    ######################################################################################

    # ##OPTIONAL MODIFICATION FOR ONLY LAST 10##
    # standings = standings[-10:]
    # t_times = t_times[-10:]
    # entrant_counts = entrant_counts[-10:]

    ########MODIFICATION FOR NORMALIZED TIMES#########
    t_times = np.arange(len(t_times))

    ##############
    # test plot
    ##############

    dpi = 124
    # fig = plt.figure(dpi=dpi, figsize=(3,1))
    fig = plt.figure(dpi=dpi, figsize=(16,5.33))
    ax1 = plt.subplot(111)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    px, py = fig.get_size_inches() * dpi
    ax1.axis('off')

    ########### format size of graph #################
    xmin = np.min(t_times) - np.ptp(t_times) / np.size(t_times)
    xmax = np.max(t_times) + np.ptp(t_times) / np.size(t_times)
    ax1.set_xlim([xmin, xmax])
    ##################################################

    barwidth = 0.5
    # barwidth = 5*24*3600

    ############# plot the bar for tourneys entered ###########
    # region
    truth_array = standings > 0
    xvals = t_times[truth_array][::-1]
    # print(xvals)
    yvals = np.zeros(len(entrant_counts[truth_array][::-1])) + 1


    bar_formatting = {
        'width' : barwidth,
        # 'color' : '#fcd720',
        'color' : 'black',
        'alpha' : 1,
        'joinstyle' : 'round'
    }
    ax1.bar(xvals, yvals, **bar_formatting)

    # endregion
    #########################################################

    ############# plot the bar for tourneys NOT entered ###########
    # region
    truth_array = ~(standings > 0)
    xvals = t_times[truth_array][::-1]
    yvals = np.zeros(len(entrant_counts[truth_array][::-1]))+1

    bar_formatting = {
        'width' : barwidth,
        'color' : 'black',
        'alpha' : 0.8
    }
    ax1.bar(xvals, yvals, **bar_formatting)

    # endregion
    #########################################################

    ############# plot the placements #############
    # region
    ## ms math ##
    barwidth_perc_of_img = barwidth / np.ptp([xmin, xmax]) 
    barwidth_in_pix = barwidth_perc_of_img * px
    markersize = barwidth_in_pix / 2
    #############
    truth_array = (standings > 0)
    xvals = t_times[truth_array][::-1]
    yvals = entrant_counts[truth_array][::-1] - standings[truth_array][::-1]
    yvals = yvals / entrant_counts[truth_array][::-1]
    plot_formatting = {
        'linestyle' : '-',
        'linewidth' : markersize / 7,
        'marker' : 'o',
        'ms' : markersize, ####REMOVE THE /2
        'color' : '#cd0024'  # BAN red
    }

    ax1.plot(xvals, yvals, **plot_formatting)
    # endregion
    ###############################################


    ############# plot the text ###################
    # region
    truth_array = (standings > 0)
    for i,j,k in zip(xvals,standings[truth_array][::-1], yvals):
        ax1.annotate(str(j),     xy =(i, k), color='white',
                            fontsize=markersize, weight='heavy',
                            horizontalalignment='center',
                            verticalalignment='center_baseline')
    # endregion

    # region Veil nonsense for transparency
    # def add_veil(ax, top, n_steps=20, color='white'):
    #     starts, height = np.linspace(0, top, n_steps, endpoint=False, retstep=True)
    #     rects = [Rectangle((0, s), 1, height, facecolor=color, zorder=2.01,
    #                         alpha=(1-(n_a/n_steps)), transform=ax.transAxes)
    #             for n_a, s in enumerate(starts)]
    #     for r in rects:
    #         ax.add_patch(r)

    # add_veil(ax1, 1, 100, 'red')

    # ax2 = plt.subplot(212)
    # endregion
    ############# plot the Title Bar ###################
    # region
    ywidth = np.ptp(ax1.get_ylim())
    extra = ywidth*0.66
    ax1.set_ylim(bottom=0-extra)
    ax1.add_patch(Rectangle((0,0), 1, 0.4, color='black', transform=ax1.transAxes))
    titletext= "Alltime BAN Placements"
    kwargs = {
        'color' : '#fcd720',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize' : py/12
    }
    ax1.text(0.5, 0.2, titletext, **kwargs)
    # endregion
    ####################################################

    # ywidth = yw
    # yw + x*yw = 
    # plt.title("Ban Result")
    plt.savefig(savename, bbox_inches=0, transparent=True)
    plt.close()
    # plt.show()
    return None

def make_first_timer_statspage_graphic(savename):
    """
    Makes a larger graphic suited for a statspage for
    a player with no data

    needs to be dramatically improved visually
    (12/2/2022)
    """
    dpi = 124
    # fig = plt.figure(dpi=dpi, figsize=(3,1))
    fig = plt.figure(dpi=dpi, figsize=(16,5.33))
    ax1 = plt.subplot(111)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    px, py = fig.get_size_inches() * dpi
    ax1.axis('off')


    textbody= "A NEW \n CHALLENGER \n APPROACHES"
    kwargs = {
        'color' : 'black',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontsize' : py/10
    }
    ax1.text(0.5, 0.5, textbody, **kwargs)
    plt.savefig(savename, bbox_inches=0, transparent=True)
    plt.close()
    return None

def make_onscreen_bar_graphic(df, p_id, savename):
    """
    Makes a graphic suited to be displayed in a small space onscreen,
    displaying recent tourney performance over time.

    With minor changes, can use time or normalized x axis, and 
    change height of bars to either be normalized to 1 or
    show entrant count
    """
    standings = df[df['p_id'] == p_id]['p_standing'].values.astype(int)
    t_names = df[df['p_id'] == p_id]['t_name'].values.astype(str)
    t_times = df[df['p_id'] == p_id]['t_starttime'].values.astype(int)
    # t_times = np.arange(len(t_times))
    entrant_counts = df[df['p_id'] == p_id]['entrant_count'].values.astype(int)

    ############## fill arrays for tourneys attended, tourneys not attended, etc #########
    ######################################################################################
    # region
    all_tourney_times = np.unique(df['t_starttime'].values)

    standings = np.array([], dtype=int)
    t_times = np.array([], dtype=int)
    entrant_counts = np.array([], dtype=int)

    for tourney_time in all_tourney_times:
        # is_right_tourney = df['t_starttime'] == tourney_time
        # has_player = df['p_id'] == p_id
        relevant_df = df[df['t_starttime'] == tourney_time]
        assert np.size(np.unique(relevant_df['entrant_count'].values)) == 1, 'same tourney diff entrant counts'
        entrant_count = relevant_df['entrant_count'].values[0]
        if len(relevant_df[relevant_df['p_id'] == p_id]) > 0:
            standing = relevant_df[relevant_df['p_id'] == p_id]['p_standing'].values[0]
        else:
            standing = -1

        standings = np.append(standings, standing)
        t_times = np.append(t_times, tourney_time)
        entrant_counts = np.append(entrant_counts, entrant_count)
    # endregion
    ######################################################################################

    ##OPTIONAL MODIFICATION FOR ONLY LAST 10##
    standings = standings[-10:]
    t_times = t_times[-10:]
    entrant_counts = entrant_counts[-10:]

    ########MODIFICATION FOR NORMALIZED TIMES#########
    t_times = np.arange(len(t_times))

    ##############
    # test plot
    ##############

    dpi = 100
    fig = plt.figure(dpi=dpi, figsize=(3,1))
    # fig = plt.figure(dpi=dpi, figsize=(16,5.33))
    ax1 = plt.subplot(111)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    px, py = fig.get_size_inches() * dpi
    ax1.axis('off')

    ########### format size of graph #################
    xmin = np.min(t_times) - np.ptp(t_times) / np.size(t_times)
    xmax = np.max(t_times) + np.ptp(t_times) / np.size(t_times)
    ax1.set_xlim([-1, len(t_times)])
    ##################################################

    barwidth = 0.5
    ############# plot the bar for tourneys entered ###########
    # region
    truth_array = standings > 0
    xvals = t_times[truth_array][::-1]
    yvals = np.zeros(len(entrant_counts[truth_array][::-1])) + 1


    bar_formatting = {
        'width' : barwidth,
        'color' : '#fcd720',
        # 'color' : 'black',
        'alpha' : 1,
        'joinstyle' : 'round'
    }
    ax1.bar(xvals, yvals, **bar_formatting)

    # endregion
    #########################################################

    ############# plot the bar for tourneys NOT entered ###########
    # region
    truth_array = ~(standings > 0)
    xvals = t_times[truth_array][::-1]
    yvals = np.zeros(len(entrant_counts[truth_array][::-1]))+1

    bar_formatting = {
        'width' : barwidth,
        'color' : 'black',
        'alpha' : 0.8
    }
    ax1.bar(xvals, yvals, **bar_formatting)

    # endregion
    #########################################################

    ############# plot the placements #############
    # region
    ## ms math ##
    barwidth_perc_of_img = barwidth / np.ptp([xmin, xmax]) 
    barwidth_in_pix = barwidth_perc_of_img * px
    markersize = barwidth_in_pix / 2
    #############
    truth_array = (standings > 0)
    xvals = t_times[truth_array][::-1]
    yvals = entrant_counts[truth_array][::-1] - standings[truth_array][::-1]
    yvals = yvals / entrant_counts[truth_array][::-1]
    plot_formatting = {
        'linestyle' : '-',
        'linewidth' : markersize / 10,
        'marker' : 'o',
        'ms' : markersize/1.5, ####REMOVE THE /2
        'color' : '#cd0024'  # BAN red
    }

    ax1.plot(xvals, yvals, **plot_formatting)
    # endregion
    ###############################################


    ############# plot the text ###################
    # region
    # truth_array = (standings > 0)
    # for i,j,k in zip(xvals,standings[truth_array][::-1], yvals):
    #     ax1.annotate(str(j),     xy =(i, k), color='white',
    #                         fontsize=markersize, weight='heavy',
    #                         horizontalalignment='center',
    #                         verticalalignment='center_baseline')
    # endregion

    # region Veil nonsense for transparency
    # def add_veil(ax, top, n_steps=20, color='white'):
    #     starts, height = np.linspace(0, top, n_steps, endpoint=False, retstep=True)
    #     rects = [Rectangle((0, s), 1, height, facecolor=color, zorder=2.01,
    #                         alpha=(1-(n_a/n_steps)), transform=ax.transAxes)
    #             for n_a, s in enumerate(starts)]
    #     for r in rects:
    #         ax.add_patch(r)

    # add_veil(ax1, 1, 100, 'red')

    # ax2 = plt.subplot(212)
    # endregion
    ############# plot the Title Bar ###################
    # region
    ywidth = np.ptp(ax1.get_ylim())
    extra = ywidth*0.66
    ax1.set_ylim(bottom=0-extra)
    ax1.add_patch(Rectangle((0,0), 1, 0.4, color='black', transform=ax1.transAxes))
    titletext= "Recent BAN Placements"
    kwargs = {
        'color' : '#fcd720',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 10,
    }
    ax1.text(0.5, 0.2, titletext, **kwargs)
    # endregion
    ####################################################

    # ywidth = yw
    # yw + x*yw = 
    # plt.title("Ban Result")
    plt.savefig(savename, bbox_inches=0, transparent=True)
    plt.close()
    # plt.show()
    return None

def make_onscreen_placement_graphic(df, p_id, savename):
    """
    Makes a graphic suited to be displayed in a small space onscreen,
    displaying best historical placement.
    """

    standings = df[df['p_id'] == p_id]['p_standing'].values.astype(int)
    t_names = df[df['p_id'] == p_id]['t_name'].values.astype(str)
    t_times = df[df['p_id'] == p_id]['t_starttime'].values.astype(int)
    # t_times = np.arange(len(t_times))
    entrant_counts = df[df['p_id'] == p_id]['entrant_count'].values.astype(int)

    ############## fill arrays for tourneys attended, tourneys not attended, etc #########
    ######################################################################################

    all_tourney_times = np.unique(df['t_starttime'].values)

    standings = np.array([], dtype=int)
    t_times = np.array([], dtype=int)
    entrant_counts = np.array([], dtype=int)

    for tourney_time in all_tourney_times:
        # is_right_tourney = df['t_starttime'] == tourney_time
        # has_player = df['p_id'] == p_id
        relevant_df = df[df['t_starttime'] == tourney_time]
        assert np.size(np.unique(relevant_df['entrant_count'].values)) == 1, 'same tourney diff entrant counts'
        entrant_count = relevant_df['entrant_count'].values[0]
        if len(relevant_df[relevant_df['p_id'] == p_id]) > 0:
            standing = relevant_df[relevant_df['p_id'] == p_id]['p_standing'].values[0]
        else:
            standing = -1

        standings = np.append(standings, standing)
        t_times = np.append(t_times, tourney_time)
        entrant_counts = np.append(entrant_counts, entrant_count)

    ##############
    # test plot
    ##############

    dpi = 100
    fig = plt.figure(dpi=dpi, figsize=(3,1))
    # fig = plt.figure(dpi=dpi, figsize=(16,5.33))
    ax1 = plt.subplot(111)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    px, py = fig.get_size_inches() * dpi
    ax1.axis('off')
    toptext = "Highest BAN Placement"
    placement = np.min(standings[standings>-1])

    import matplotlib.patheffects as PathEffects

    kwargs = {
        'color' : 'black',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 5,
    }
    # tt = ax1.text(0.5, 0.8, toptext, **kwargs)
    # tt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])

    tt = ax1.text(0.5, 0.7, placement, **kwargs)
    tt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])


    ax1.add_patch(Rectangle((0,0), 1, 0.4, color='black', transform=ax1.transAxes))
    kwargs = {
        'color' : '#fcd720',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 10,
    }
    ax1.text(0.5, 0.2, toptext, **kwargs)




    plt.savefig(savename, bbox_inches=0, transparent=True)
    plt.close()
    return None

def make_onscreen_tcount_graphic(df, p_id, savename):
    """
    Makes a graphic suited to be displayed in a small space onscreen,
    displaying number of relevant tournaments entered.
    """  

    standings = df[df['p_id'] == p_id]['p_standing'].values.astype(int)
    t_names = df[df['p_id'] == p_id]['t_name'].values.astype(str)
    t_times = df[df['p_id'] == p_id]['t_starttime'].values.astype(int)
    # t_times = np.arange(len(t_times))
    entrant_counts = df[df['p_id'] == p_id]['entrant_count'].values.astype(int)

    ############## fill arrays for tourneys attended, tourneys not attended, etc #########
    ######################################################################################

    all_tourney_times = np.unique(df['t_starttime'].values)

    standings = np.array([], dtype=int)
    t_times = np.array([], dtype=int)
    entrant_counts = np.array([], dtype=int)

    for tourney_time in all_tourney_times:
        # is_right_tourney = df['t_starttime'] == tourney_time
        # has_player = df['p_id'] == p_id
        relevant_df = df[df['t_starttime'] == tourney_time]
        assert np.size(np.unique(relevant_df['entrant_count'].values)) == 1, 'same tourney diff entrant counts'
        entrant_count = relevant_df['entrant_count'].values[0]
        if len(relevant_df[relevant_df['p_id'] == p_id]) > 0:
            standing = relevant_df[relevant_df['p_id'] == p_id]['p_standing'].values[0]
        else:
            standing = -1

        standings = np.append(standings, standing)
        t_times = np.append(t_times, tourney_time)
        entrant_counts = np.append(entrant_counts, entrant_count)

    ##############
    # test plot
    ##############

    dpi = 100
    fig = plt.figure(dpi=dpi, figsize=(3,1))
    # fig = plt.figure(dpi=dpi, figsize=(16,5.33))
    ax1 = plt.subplot(111)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    px, py = fig.get_size_inches() * dpi
    ax1.axis('off')
    toptext = "BANs Entered"
    placement = len(standings[standings>0])

    import matplotlib.patheffects as PathEffects

    kwargs = {
        'color' : 'black',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 5,
    }
    # tt = ax1.text(0.5, 0.8, toptext, **kwargs)
    # tt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])

    tt = ax1.text(0.5, 0.7, placement, **kwargs)
    tt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])


    ax1.add_patch(Rectangle((0,0), 1, 0.4, color='black', transform=ax1.transAxes))
    kwargs = {
        'color' : '#fcd720',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 10,
    }
    ax1.text(0.5, 0.2, toptext, **kwargs)




    plt.savefig(savename, bbox_inches=0, transparent=True)
    plt.close()
    return None

def make_onscreen_newplayer_graphic(savename):
    """
    Makes a graphic suited to be displayed in a small space onscreen,
    displaying an image for a player with no historical data.
    """    

    dpi = 100
    fig = plt.figure(dpi=dpi, figsize=(3,1))
    # fig = plt.figure(dpi=dpi, figsize=(16,5.33))
    ax1 = plt.subplot(111)
    plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, 
                hspace = 0, wspace = 0)
    plt.margins(0,0)
    px, py = fig.get_size_inches() * dpi
    ax1.axis('off')
    toptext = "Player Data"
    placement = "New \n Challenger"

    kwargs = {
        'color' : 'black',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 10,
    }
    # tt = ax1.text(0.5, 0.8, toptext, **kwargs)
    # tt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])

    tt = ax1.text(0.5, 0.7, placement, **kwargs)
    tt.set_path_effects([PathEffects.withStroke(linewidth=2, foreground='w')])


    ax1.add_patch(Rectangle((0,0), 1, 0.4, color='black', transform=ax1.transAxes))
    kwargs = {
        'color' : '#fcd720',
        'ha' : 'center',
        'va' : 'center',
        'transform' : ax1.transAxes,
        'fontweight' : 'heavy',
        'fontsize'  : py * 1.5 / 10,
    }
    ax1.text(0.5, 0.2, toptext, **kwargs)

    plt.savefig(savename, bbox_inches=0, transparent=True)
    plt.close()
    return None

def update_graphic_and_statpage_data(df, p_id, file_location, playernum=1):
    """
    Updates the various files the program makes available to OBS for a single player
    """

    ban_count = get_player_number_bans(df, p_id)
    deletionlist1 = glob.glob(file_location + fr'\statspage\*.txt')
    deletionlist2 = glob.glob(file_location + fr'\statspage\slideshow_p{playernum}\*.png')
    deletionlist3 = glob.glob(file_location + fr'\statspage\onscreen_p{playernum}\*.png')
    files_to_delete = deletionlist1 + deletionlist2 + deletionlist3
    for file in files_to_delete:
        os.remove(file)
    
    
    if ban_count > 0:

        # update best tourney placement
        best_placement = get_player_highest_placement(df, p_id)
        filename = fr"{file_location}/statspage/player{playernum}bestplacement.txt"
        f = open(filename, "w")
        f.write(fr'Best Placement : {best_placement}')
        f.close()

        #update number of bans
        filename = fr"{file_location}/statspage/player{playernum}numberBANs.txt"
        f = open(filename, "w")
        f.write(fr'BANs Entered : {ban_count}')
        f.close()

        #update the graph
        filename = fr'{file_location}\statspage\slideshow_p{playernum}\recentbargraph.png'
        # print(file_location)
        make_recent_tourney_bar_graph(df, p_id, filename)
        # print(file_location)

        # update the onscreen graphics
        filename = fr'{file_location}\statspage\onscreen_p{playernum}\3recentbargraph.png'
        make_onscreen_bar_graphic(df, p_id, filename)
        filename = fr'{file_location}\statspage\onscreen_p{playernum}\2topplacement.png'
        make_onscreen_placement_graphic(df, p_id, filename)
        filename = fr'{file_location}\statspage\onscreen_p{playernum}\1bansentered.png'
        make_onscreen_tcount_graphic(df, p_id, filename)

    
    else:
        # update best tourney placement
        best_placement = "Wait and see..."
        filename = fr"{file_location}\statspage\player{playernum}bestplacement.txt"
        f = open(filename, "w")
        f.write(fr'Best Placement : {best_placement}')
        f.close()

        #update number of bans
        filename = fr"{file_location}\statspage\player{playernum}numberBANs.txt"
        f = open(filename, "w")
        f.write(fr'BANs Entered : First Time!')
        f.close()

        #update the graph
        filename = fr'{file_location}\statspage\slideshow_p{playernum}\recentbargraph.png'
        # print(file_location)
        make_first_timer_statspage_graphic(filename)
        # print(file_location)

        #update the onscreen graphics
        filename = fr'{file_location}\statspage\onscreen_p{playernum}\newchallenger.png'
        make_onscreen_newplayer_graphic(filename)

