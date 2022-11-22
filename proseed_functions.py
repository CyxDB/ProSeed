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
    t_times = np.array([], dtype=int)
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
    









