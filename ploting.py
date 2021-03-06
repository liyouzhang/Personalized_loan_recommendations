from math import pi
import plotly
plotly.tools.set_credentials_file(username='PUT_USERNAME', api_key='PUT_API_KEY')
import plotly.plotly as py
import plotly.graph_objs as go
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from matplotlib_venn import venn3, venn3_circles


def plot_2D_reduced_X(X_reduced):
    '''plot for 2D - PCA'''
    fig, ax = plt.subplots(1, figsize=(8, 6))
    ax.scatter(X_reduced[:, 0], X_reduced[:, 1]);
    ax.set_title("Scatterplot in PCA 2-Plane")
    ax.set_xlabel("First Principal Component")
    ax.set_ylabel("Second Principal Component")
    plt.show()

def plotly_3D_reduced_X(X_reduced):
    '''use plotly to visualize the 3D reduced X'''
    trace1 = go.Scatter3d(
    x=X_reduced[:,0],
    y=X_reduced[:,1],
    z=X_reduced[:,2],
    mode='markers',
    marker=dict(
        size=12,
        line=dict(
            color='rgba(217, 217, 217, 0.14)',
            width=0.5
            ),
        opacity=0.8
        )
    )
    data = [trace1]
    layout = go.Layout(
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0
        )
    )
    fig = go.Figure(data=data, layout=layout)
    py.iplot(fig, filename='simple-3d-scatter')


def plot_2D_kmeans(X_reduced,y,xlim_left,xlim_right,ylim_down,ylim_up):
    '''plot for kmeans results, adjust ax lim to zoom in/out'''
    fig, ax = plt.subplots(figsize=(8,6))
    ax.scatter(X_reduced[:,0],X_reduced[:,1],c=y,linewidths=0)
    ax.set_xlim(xlim_left,xlim_right)
    ax.set_ylim(ylim_down,ylim_up)
    ax.set_title("Scatterplot in PCA 2-Plane with clustering results")
    plt.show()


def plot_3D_kmeans(X_reduced,y,xlabel,ylabel,zlabel,title,xlim=None,ylim=None,zlim=None):
    '''use matplotlib to plot the 3D kmeans cluster results'''
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    # for c, m in [('r', 'o'), ('b', '^')]:
    xs=X_reduced[:,0]
    ys=X_reduced[:,1]
    zs=X_reduced[:,2]
    ax.scatter(xs, ys, zs, c=y, marker='^')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    ax.set_title(title)
    if xlim != None:
        ax.set_xlim(xlim[0],xlim[1])
    if ylim != None:
        ax.set_ylim(ylim[0],ylim[1])
    if zlim != None:
        ax.set_zlim(zlim[0],zlim[1])
    plt.show()

def matplotlib_3D_X_reduced(X_reduced,label1="First Principle Component",label2="Second Principle Component",label3="Third Principle Component",title="Scatterplot in PCA 3D-Plane"):
    '''use matplotlib to plot the 3D PCA results'''
    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111, projection='3d')
    # for c, m in [('r', 'o'), ('b', '^')]:
    xs=X_reduced[:,0]
    ys=X_reduced[:,1]
    zs=X_reduced[:,2]
    ax.scatter(xs, ys, zs, c='green', marker='^')
    ax.set_xlabel(label1)
    ax.set_ylabel(label2)
    ax.set_zlabel(label3)
    ax.set_title(title)
    plt.show()


def plot_radar(df, figname=None, dpi=64, category=False, num_of_cat=False,ylim=(0,1)):
    '''plot spider graph to interpret clustering results
    INPUT - df: cluster number as index'''
    # initialize the figure
    my_dpi = dpi
    plt.figure(figsize=(1333/my_dpi,900/my_dpi), dpi=my_dpi)
    # plt.tight_layout()

    # Create a color palette:
    my_palette = plt.cm.get_cmap("Set1", len(df.index))

    for row in range(0, len(df.index)):
        make_spider(df=df, row=row, title='group{}'.format(
            row), color=my_palette(row), category=category, num_of_cat=num_of_cat,ylim=ylim)
    if figname != None:
        plt.savefig('{}.png'.format(figname))


def make_spider(df, row, title, color, category, num_of_cat,ylim):
    '''plot spider graph to interpret clustering results. called in plot_radar function'''
    # number of variable
    categories = list(df)
    if category == True:
        cat = []
        for c in categories:
            cat.append(c.split("_")[-1])
        categories = cat
    elif num_of_cat == True:
        cat = []
        for c in categories:
            cat.append(" ".join(c.split("_")[2:-1]))
        categories = cat

    N = len(categories)

    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]

    # Initialise the spider plot
    ax = plt.subplot(2, 3, row+1, polar=True)

    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)

    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='grey', size=14)

    # Draw ylabels
    ax.set_rlabel_position(0)
    #plt.yticks([10,20,30], ["10","20","30"], color="grey", size=7)
    plt.ylim(ylim[0],ylim[1])

    # Ind1
    values = df.loc[row].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color=color, alpha=0.4)

    # Add a title
    plt.title(title, size=20, color=color, y=1.1)
    plt.savefig('group{}'.format(row))



def plot_venn_3(a, b, c, a_and_b, a_and_c, b_and_c, a_and_b_and_c, a_label="Group A", b_label="Group B", c_label="Group C"):
    '''use matplotlib venn library to plot three groups interactions'''
    position0 = int((a - a_and_b - a_and_c + a_and_b_and_c)/1000)
    position1 = int((b - b_and_c - a_and_b + a_and_b_and_c)/1000)
    position2 = int((a_and_b - a_and_b_and_c)/1000)
    position3 = int((c - a_and_c - b_and_c + a_and_b_and_c)/1000)
    position4 = int((a_and_c - a_and_b_and_c)/1000)
    position5 = int((b_and_c - a_and_b_and_c)/1000)
    position6 = int(a_and_b_and_c/1000)
 

    # Line style: can be 'dashed' or 'dotted' for example
    v = venn3(subsets=(position0, position1, position2, position3, position4,
                       position5, position6), set_labels=(a_label, b_label, c_label))
    c = venn3_circles(subsets=(position0, position1, position2, position3, position4,
                               position5, position6), linestyle='dashed', linewidth=1, color="grey")
    plt.savefig('outliers.png')
    plt.show()


def plot_lifespan_trend(df,purchase,donations,deposits):
    '''[summary]
    plot the trend of behaviors over lifespan of each user group

    Arguments:
        df {pandas dataframe}
        purchase {list of column names } -- columns that describe the purchase behaviors
        donations {list of column names } -- columns that describe the donations behaviors
        deposits {list of column names } -- columns that describe the deposits behaviors
    '''

    age = df.loc[0,['ACCOUNT_AGE_MONTHS']]
    values = df.loc[0,purchase]
    donation_values = df.loc[0,donations]
    deposit_values = df.loc[0,deposits]
    last_login = df.loc[0,"last_login_today_months"]
    plt.figure(figsize=(8,6))
    ax1 = plt.subplot(1,1,1)

    ax1.scatter((1,12,age),(values[0],values[1],values[2]),marker='^',s=30,label='purchase')
    ax1.plot((1,12,age),(values[0],values[1],values[2]))
    ax1.scatter((1,12,age),(donation_values[0],donation_values[1],donation_values[2]),marker='*',s=30,label='donation')
    ax1.plot((1,12,age),(donation_values[0],donation_values[1],donation_values[2]))
    ax1.scatter((1,12,age),(deposit_values[0],deposit_values[1],deposit_values[2]),marker='o',s=30,label='deposit')
    ax1.plot((1,12,age),(deposit_values[0],deposit_values[1],deposit_values[2]))

    ax1.vlines(1,-30,175,linestyles='--',label='first day')
    ax1.vlines(12,-30,175,linestyles='--',label='first year')
    ax1.vlines(age,-30,175,linestyles='--',label='account age')
    ax1.vlines(age-last_login,-30,175,linestyles=':',label='last login month')
    ax1.set_title("Change of behaviors over lifetime - group 0")
    ax1.set_xlim(-20,106)
    ax1.set_ylabel('$')
    ax1.set_xlabel('month')
    plt.legend()
    plt.savefig('group0.png')
    plt.show()

    for i in range(1,6):
        age = df.loc[i,['ACCOUNT_AGE_MONTHS']]
        values = df.loc[i,purchase]
        donation_values = df.loc[i,donations]
        deposit_values = df.loc[i,deposits]
        plt.figure(figsize=(8,6))
        ax = plt.subplot(1,1,1,sharex=ax1)
        ax.scatter((1,12,age),(values[0],values[1],values[2]),marker='^',s=30,label='purchase')
        ax.plot((1,12,age),(values[0],values[1],values[2]))
        ax.scatter((1,12,age),(donation_values[0],donation_values[1],donation_values[2]),marker='*',s=30,label='donation')
        ax.plot((1,12,age),(donation_values[0],donation_values[1],donation_values[2]))
        ax.scatter((1,12,age),(deposit_values[0],deposit_values[1],deposit_values[2]),marker='o',s=30,label='deposit')
        ax.plot((1,12,age),(deposit_values[0],deposit_values[1],deposit_values[2]))
        ax.vlines(1,-30,175,linestyles='--',label='first day')
        ax.vlines(12,-30,175,linestyles='--',label='first year')
        ax.vlines(age,-30,175,linestyles='--',label='account age')
        ax.vlines(age-last_login,-30,175,linestyles=':',label='last login month')
        ax.set_title("Change of behaviors over lifetime - group {}".format(i))
        ax.set_xlim(-20,106)
        ax.set_ylabel('$')
        ax.set_xlabel('month')
        plt.legend(loc='upper right')
        plt.savefig('group{}.png'.format(i))
        plt.show()
