import sys
import shutil
import os
import zipfile
import wget


def read_seq_list():
    if os.path.isfile('seq.txt'):
        seq_file = open('seq.txt', 'r')
        return seq_file.readlines()
    else:
        print('[**ERROR**] Sequences File Dose NOT Exist !')


# ========================================================================================================
def download_all_sequences(seq_mode, out_path):

    # Read all sequences names
    files_list = read_seq_list()
    count = 0
    total_seq = len(files_list)
    for line in files_list:
        count += 1
        seq_name = line.rstrip('\n')
        print('\nSequence ', count, ' of ', total_seq, ' : ',  seq_name)

        # for each sequence:
        # --- (0) check if it was downloaded before
        if os.path.exists(out_path+seq_name):
            print('=> ', seq_name, ' Already exists.\n')
        else:
            # --- (1) download the sequence
            download_seq(seq_name, seq_mode, out_path)

            # --- (2) Extract the file
            print("---- Unzipping")
            with zipfile.ZipFile(out_path+seq_name+'.zip', "r") as zip_ref:
                zip_ref.extractall(out_path+seq_name)

            # --- (3) Delete Downloaded files
            print("---- Cleaning up !")
            shutil.rmtree(out_path+seq_name)
            os.remove(out_path+seq_name+'.zip')

    print('------------------------------------')


# ========================================================================================================
def download_seq(seq_name, download_mode, out_path):
    print('======> Downloading:', seq_name)

    # create the directory for download
    download_dir = out_path+'/'+seq_name
    if ~os.path.exists(download_dir):
        os.mkdir(download_dir)

    url_easy_left = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Easy/image_left.zip"
    url_easy_right = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Easy/image_right.zip"
    url_hard_left = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Hard/image_left.zip"
    url_hard_right = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Hard/image_right.zip"

    if download_mode == 1:
        # easy sequences only
        # ================================================================================================
        # -- create the easy folder
        if os.path.exists(download_dir+'/Easy'):
            os.rmdir(download_dir+'/Easy')
        os.mkdir(download_dir+'/Easy')

        print('=> Downloading', seq_name+ ' Easy - Left')
        filename = wget.download(url_easy_left, download_dir+'/Easy/image_left.zip', bar=bar_custom)
        print('=> Downloading', seq_name + ' Easy - Right')
        filename = wget.download(url_easy_right, download_dir + '/Easy/image_right.zip', bar=bar_custom)
        print("\n----", seq_name+" easy seq. ", ' ==> Downloaded !')

        print("---- Unzipping left images folder")
        with zipfile.ZipFile(download_dir + '/Easy/image_left.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Easy/image_left')

        print("---- Unzipping right images folder")
        with zipfile.ZipFile(download_dir + '/Easy/image_right.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Easy/image_right')

    elif download_mode == 2:
        # hard sequences only
        # ================================================================================================
        # -- create the hard folder
        if os.path.exists(download_dir + '/Hard'):
            os.rmdir(download_dir + '/Hard')
        os.mkdir(download_dir + '/Hard')

        print('=> Downloading', seq_name + ' Hard - Left')
        filename = wget.download(url_hard_left, download_dir + '/Hard/image_left.zip', bar=bar_custom)
        print('=> Downloading', seq_name + ' Hard - Right')
        filename = wget.download(url_hard_right, download_dir + '/Hard/image_right.zip', bar=bar_custom)
        print("\n----", seq_name + " hard seq. ", ' ==> Downloaded !')

        print("---- Unzipping left images folder")
        with zipfile.ZipFile(download_dir + '/Hard/image_left.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Hard/image_left')

        print("---- Unzipping right images folder")
        with zipfile.ZipFile(download_dir + '/Hard/image_right.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Hard/image_right')

    else:
        # Both hard and easy sequences
        # ================================================================================================
        # -- create the easy folder
        if os.path.exists(download_dir + '/Easy'):
            os.rmdir(download_dir + '/Easy')
        os.mkdir(download_dir + '/Easy')

        print('=> Downloading', seq_name + ' Easy - Left')
        filename = wget.download(url_easy_left, download_dir + '/Easy/image_left.zip', bar=bar_custom)
        print('=> Downloading', seq_name + ' Easy - Right')
        filename = wget.download(url_easy_right, download_dir + '/Easy/image_right.zip', bar=bar_custom)
        print("\n----", seq_name + " easy seq. ", ' ==> Downloaded !')

        print("---- Unzipping left images folder")
        with zipfile.ZipFile(download_dir + '/Easy/image_left.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Easy/image_left')

        print("---- Unzipping right images folder")
        with zipfile.ZipFile(download_dir + '/Easy/image_right.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Easy/image_right')

        # ================================================================================================
        # -- create the hard folder
        if os.path.exists(download_dir + '/Hard'):
            os.rmdir(download_dir + '/Hard')
        os.mkdir(download_dir + '/Hard')

        print('=> Downloading', seq_name + ' Hard - Left')
        filename = wget.download(url_hard_left, download_dir + '/Hard/image_left.zip', bar=bar_custom)
        print('=> Downloading', seq_name + ' Hard - Right')
        filename = wget.download(url_hard_right, download_dir + '/Hard/image_right.zip', bar=bar_custom)
        print("\n----", seq_name + " hard seq. ", ' ==> Downloaded !')

        print("---- Unzipping left images folder")
        with zipfile.ZipFile(download_dir + '/Hard/image_left.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Hard/image_left')

        print("---- Unzipping right images folder")
        with zipfile.ZipFile(download_dir + '/Hard/image_right.zip', "r") as zip_ref:
            zip_ref.extractall(download_dir + '/Hard/image_right')


# ========================================================================================================
def bar_custom(current, total, width=80):
    progress_message = "---- Downloading: %d%% [%d / %d] MegaBytes" % (current / total * 100, current/1e6, total/1e6)
    # Don't use print() as it will print in new line every time.
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


# ========================================================================================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('Very few command line arguments, please provide output path and download mode')
        sys.exit()
    else:
        print('[INFO] Output Path: \t' + sys.argv[1])
        mode = 0
        if sys.argv[2] == 'easy':
            mode = 1
            print('[INFO] Download Mode: \tEasy Sequences')
        elif sys.argv[2] == 'hard':
            mode = 2
            print('[INFO] Download Mode: \tHard Sequences')
        else:
            mode = 0
            print('[INFO] Download Mode: \tEasy & Hard Sequences')

        print('\n\n')
        download_all_sequences(mode, sys.argv[1])

