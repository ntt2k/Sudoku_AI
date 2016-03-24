import os
# import subprocess

for root, dirs, files in os.walk("."):
    for name in files:
        # print(name.strip(".txt"))
        # print(os.path.join(root, name))
        os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_BT.txt 1800 BT".format(name, name.strip(".txt")))
        os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC.txt 900 FC".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_AC.txt 600 AC".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_MRV.txt 600 MRV".format(name, name.strip(".txt")))
        os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC_MRV.txt 600 FC MRV".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC_DH.txt 3600 FC DH".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC_MRV_DH.txt 600 FC MRV DH".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_LCV.txt 900 LCV".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC_MRV_LCV.txt 600 FC MRV LCV".format(name, name.strip(".txt")))
        # os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC_DH_LCV.txt 600 FC DH LCV".format(name, name.strip(".txt")))
        os.system("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC_MRV_DH_LCV.txt 300 FC MRV DH LCV".format(name, name.strip(".txt")))

        # subprocess.call("python3 ../scr_bin/main.py ../testfiles/{} ../outputfiles/output_{}_FC.txt 600 FC".format(name, name.strip(".txt")), shell=True)
