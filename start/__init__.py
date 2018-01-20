
import subprocess
import config

def run(ip, id, contest):

    commands = ""
    commands += "tmux kill-session -t cms;"
    if id == 0:
        commands += "tmux new-session -d -s cms -n AdminServer 'cmsAdminWebServer'\; neww -n Logs 'cmsLogService'\; neww -n RankingServer 'cmsRankingWebServer'\; neww -n ResourceService 'cmsResourceService 0 -a {}'\;".format(contest);
    else:
        commands += "tmux new-session -d -s cms -n ResourceService 'cmsResourceService {} -a {}'\;".format(id, contest);
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
