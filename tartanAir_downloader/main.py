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

        download_seq(seq_name, seq_mode, out_path)

        # # --- (2) Extract the file
        # print("---- Unzipping")
        # with zipfile.ZipFile(out_path+seq_name+'.zip', "r") as zip_ref:
        #     zip_ref.extractall(out_path+seq_name)
        #
        # # --- (3) Delete Downloaded files
        # print("---- Cleaning up !")
        # shutil.rmtree(out_path+seq_name)
        # os.remove(out_path+seq_name+'.zip')

    print('------------------------------------')


# ========================================================================================================
def download_seq(seq_name, download_mode, out_path):
    print('======> Downloading:', seq_name)

    # create the directory for download
    download_dir = out_path+seq_name

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    url_easy_left = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Easy/image_left.zip"
    url_easy_right = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Easy/image_right.zip"
    url_hard_left = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Hard/image_left.zip"
    url_hard_right = "https://tartanair.blob.core.windows.net/tartanair-release1/" + seq_name + "/Hard/image_right.zip"

    if download_mode == 1:
        # easy sequences only
        # ================================================================================================
        # -- create the easy folder
        if not os.path.exists(download_dir+'/Easy'):
            os.mkdir(download_dir+'/Easy')

        download_zip_file(seq_name, url_easy_left, download_dir, 'Easy', 'left')
        download_zip_file(seq_name, url_easy_right, download_dir, 'Easy', 'right')
        print("\n----", seq_name+" easy seq. ", ' ==> Downloaded !')

    elif download_mode == 2:
        # hard sequences only
        # ================================================================================================
        # -- create the hard folder
        if not os.path.exists(download_dir + '/Hard'):
            os.mkdir(download_dir + '/Hard')

        download_zip_file(seq_name, url_hard_left, download_dir, 'Hard', 'left')
        download_zip_file(seq_name, url_hard_right, download_dir, 'Hard', 'right')
        print("\n----", seq_name + " hard seq. ", ' ==> Downloaded !')

    else:
        # Both hard and easy sequences
        # ================================================================================================
        # -- create the easy folder
        if not os.path.exists(download_dir + '/Easy'):
            os.mkdir(download_dir + '/Easy')

        download_zip_file(seq_name, url_easy_left, download_dir, 'Easy', 'left')
        download_zip_file(seq_name, url_easy_right, download_dir, 'Easy', 'right')
        print("\n----", seq_name + " easy seq. ", ' ==> Downloaded !')

        # ================================================================================================
        # -- create the hard folder
        if not os.path.exists(download_dir + '/Hard'):
            os.mkdir(download_dir + '/Hard')

        download_zip_file(seq_name, url_hard_left, download_dir, 'Hard', 'left')
        download_zip_file(seq_name, url_hard_right, download_dir, 'Hard', 'right')
        print("\n----", seq_name + " hard seq. ", ' ==> Downloaded !')


# ========================================================================================================
def download_zip_file(m_seq_name, m_url, m_down_dir, m_level, m_camera):

    print('\n=> Downloading', m_seq_name + ' '+m_level+' - '+m_camera)

    # prepare the destination file names
    dst_path = m_down_dir + '/'+m_level+'/image_'+m_camera+'.zip'
    dst_folder = m_down_dir + '/'+m_level+'/image_'+m_camera

    # check if file exists
    if os.path.exists(dst_path):
        print('\n=> Already Exists.')
    else:
        # download the file if doesn't exist
        filename = wget.download(m_url, dst_path, bar=bar_custom)

        # unzip the file after download is done
        print("---- Unzipping left images folder")
        with zipfile.ZipFile(dst_path, "r") as zip_ref:
            zip_ref.extractall(dst_folder)

        # delete the zipped file
        print("---- Cleaning up !")
        os.remove(dst_path)


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

