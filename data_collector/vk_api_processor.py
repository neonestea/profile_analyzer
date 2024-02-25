import vk_api
from datetime import datetime
from .models import ProfileInfo, GroupInfo
import uuid
from .custom_logger import configure_logger, set_stdout_handler

session = vk_api.VkApi(token="vk1.a.Gi9VLR0O3w9yu6Mf30_rFTibl20zp6XMcjmn_sodhGHSH1tWW8_nYW9NZ9DavAhtQFnxA1sVeZ5b5754Rtzio8J8sDoCB6XFN4MX0QgbiN548Wc8xKFnqvv2Avqjb7O5xps2J8QSEpIwfR93NNq2aBKymo0KCdqiTSMXfKB36AT-x7xcnBjxTmvXxnaW4WVLniAlDvn2nVjDOCGcrjFS5Q")
vk = session.get_api()
date_format = "%d.%m.%Y"
logger = configure_logger()
logger = set_stdout_handler(logger)

def get_alc(id):
    if id == 0:
        return "Не указано"
    elif id == 1:
        return "Резко негативное"
    elif id == 2:
        return "Негативное"
    elif id == 3:
        return "Компромиссное"
    elif id == 4:
        return "Нейтральное"
    else:
        return "Положительное"


def get_people_main(id):
    if id == 0:
        return "Не указано"
    elif id == 1:
        return "Ум и креативность"
    elif id == 2:
        return "Доброта и честность"
    elif id == 3:
        return "Красота и здоровье"
    elif id == 4:
        return "Власть и богатство"
    elif id == 5:
        return "Смелость и упорство"
    else:
        return "Юмор и жизнелюбие"
    
def get_life_main(id):
    if id == 0:
        return "Не указано"
    elif id == 1:
        return "Семья и дети"
    elif id == 2:
        return "Карьера и деньги"
    elif id == 3:
        return "Развлечения и отдых"
    elif id == 4:
        return "Наука и исследования"
    elif id == 5:
        return "Совершенствование мира"
    elif id == 6:
        return "Саморазвитие"
    else:
        return "Красота и искусство"

def get_relation(id):
    if id == 0:
        return 'Не указано'
    elif id == 1:
        return "Не замужем/Не женат"
    elif id == 2:
        return "Встречаюсь"
    elif id == 3:
        return "Помолвлен"
    elif id == 4:
        return "Замужем/Женат"
    elif id == 5:
        return "В гражданском браке"
    elif id == 6:
        return "Влюблен"
    elif id == 7:
        return "Все сложно"
    else:
        return "В активном поиске"

def get_political(id):
    if id == 0:
        return "Не указано"
    elif id == 1:
        return "Индифферетные"
    elif id == 2:
        return "Коммунистические"
    elif id == 3:
        return "Социалистические"
    elif id == 4:
        return "Умеренные"
    elif id == 5:
        return "Либеральные"
    elif id == 6:
        return "Консервативные"
    elif id == 7:
        return "Монархические"
    elif id == 8:
        return "Ультраконсервативные"
    else:
        return "Либертарианские"
def start_collecting_info(search, links):
    logger.debug("START start_collecting_info")
    links = [el.strip() for el in links.split('\n')]
    for link in links:
        parse_profile(link, search)

def parse_profile(url, search):
    profile = check_user(url)
    logger.debug("START parse_profile")
    if profile is not None:
        parse_profile_info(profile, url, search)
    else:
        profile = check_group(url)
        members = vk.groups.getMembers(group_id = profile['id'])
        for member in members['items']:
            usr_link = 'https://vk.com/id' + str(member)
            logger.debug("Result link = %s", usr_link)
            member_profile = check_user(usr_link)
            parse_profile_info(member_profile, usr_link, search)

def parse_profile_info(profile, url, search):
    logger.debug("START parse_profile_info")
    profile_id = str(profile['id'])
    new_profile_info = ProfileInfo()
    new_profile_info.connected_search = search
    new_profile_info.link = url
    new_profile_info.country = profile['country']['title'] if 'country' in profile else "Не указано"
    new_profile_info.city = profile['city']['title'] if 'city' in profile else "Не указано"
    new_profile_info.first_name = profile['first_name'] if 'first_name' in profile else "Не указано"
    new_profile_info.last_name = profile['last_name'] if 'last_name' in profile else "Не указано"
    new_profile_info.bdate = datetime.strptime(profile['bdate'], date_format) if 'bdate' in profile else datetime.now()
    new_profile_info.interests = profile['interests'] if 'interests' in profile else "Не указано"
    new_profile_info.books = profile['books'] if 'books' in profile else "Не указано"
    new_profile_info.tv = profile['tv'] if 'tv' in profile else "Не указано"
    new_profile_info.games = profile['games'] if 'games' in profile else "Не указано"
    new_profile_info.movies = profile['movies'] if 'movies' in profile else "Не указано"
    new_profile_info.activities = profile['activities'] if 'activities' in profile else "Не указано"
    new_profile_info.music = profile['music'] if 'music' in profile else "Не указано"
    new_profile_info.status = profile['status'] if 'status' in profile else "Не указано"
    new_profile_info.military = len(profile['military']) != 0 if 'military' in profile else 0
    new_profile_info.university_name = profile['university_name'] if 'university_name' in profile else "Не указано"
    new_profile_info.faculty = "Не указано"
    new_profile_info.posts_count = get_user_posts(profile_id)
    new_profile_info.photos_count = get_user_photos(profile_id)
    if 'university' in profile and 'faculty' in profile:
        university_id = int(profile['university'])
        if university_id != 0:
            faculties = vk.database.getFaculties(university_id = university_id)
            for el in faculties['items']:
                if el['id'] == int(profile['faculty']):
                    new_profile_info.faculty = el['title']
    
    #info['graduation'] = profile['graduation'] if 'graduation' in profile else None
    new_profile_info.home_town = profile['home_town'] if 'home_town' in profile else "Не указано"
    new_profile_info.relation = get_relation(int(profile['relation'])) if 'relation' in profile else "Не указано"
    #info['schools'] = profile['schools'] if 'schools' in profile else None
    new_profile_info.sex = int(profile['sex']) if 'sex' in profile else "Не указано"
    new_profile_info.about = profile['about'] if 'about' in profile else "Не указано"
    #info['career'] = profile['career'] if 'career' in profile else None
    new_profile_info.country = profile['country']['title'] if 'country' in profile else "Не указано"
    new_profile_info.city = profile['city']['title'] if 'city' in profile else "Не указано"
    #new_profile_info.timezone = profile['timezone'] if 'timezone' in profile else "Не указано"
    new_profile_info.friends_count = get_user_friends(profile_id)
    new_profile_info.followers_count = get_user_followers(profile_id)
    new_profile_info.groups = get_user_groups(profile_id)
    new_profile_info.posts, new_profile_info.comments, new_profile_info.comments_of_other_users = get_all_user_comments(profile_id)
    #new_profile_info.occupation = profile['occupation'] if 'occupation' in profile else "Не указано"
    if 'personal' in profile:
        pers = profile['personal']
        new_profile_info.alcohol = get_alc(int(pers['alcohol'])) if 'alcohol' in pers else "Не указано"
        new_profile_info.life_main = get_life_main(int(pers['life_main'])) if 'life_main' in pers else "Не указано"
        new_profile_info.people_main = get_people_main(int(pers['people_main'])) if 'people_main' in pers else "Не указано"
        new_profile_info.political = get_political(int(pers['political'])) if 'political' in pers else "Не указано"
        new_profile_info.religion = pers['religion'] if 'religion' in pers else "Не указано"
        new_profile_info.smoking = get_alc(int(pers['smoking'])) if 'smoking' in pers else "Не указано"

    else:
        new_profile_info.alcohol = "Не указано"
        new_profile_info.life_main = "Не указано"
        new_profile_info.people_main = "Не указано"
        new_profile_info.political = "Не указано"
        new_profile_info.religion = "Не указано"
        new_profile_info.smoking = "Не указано"  
    new_profile_info.save()
    for group in new_profile_info.groups:
        new_group_info = GroupInfo()
        new_group_info.connected_search = search
        #TODO
        new_group_info.posts = 'Не указано'#get_user_wall(group)
        new_group_info.description = get_group_description(group)
        new_group_info.save()

    
def check_user(url):
    token = url.split('/')[-1]
    profile = vk.users.get(user_ids=(token), fields = "activities, about, books, bdate, career, city, country, education, exports, followers_count, has_photo, has_mobile, home_town, sex, site, schools, screen_name, status, games, interests, is_hidden_from_feed, maiden_name, military, movies, music, nickname, occupation, personal, quotes, relation, relatives, timezone, tv, universities")
    if len(profile) == 0:
            return None
    return profile[0]

def check_group(url):
    token = url.split('/')[-1]
    profile = vk.groups.getById(group_id=token)
    if len(profile) == 0:
            return None
    return profile[0]

def get_user_posts(user_id):
    posts_count = 0
    try: 
        wall = vk.wall.get(owner_id = user_id)
        posts_count = wall['count']
        return posts_count
    except vk_api.exceptions.ApiError: 
        return posts_count

def get_user_photos(user_id):
    photos_count = 0
    try: 
        photos = vk.photos.getAll(owner_id = user_id)
        photos_count = photos['count']
        return photos_count
    except vk_api.exceptions.ApiError: 
        return photos_count

def get_user_groups(user_id):
    logger.debug("START get_user_groups")
    try:
        groups = vk.users.getSubscriptions(user_id = user_id)
        return groups['groups']['items']
    except vk_api.exceptions.ApiError:
        return []
    
def process_groups_info(user_id):
    logger.debug("START process_groups_info")
    try:
        groups = vk.users.getSubscriptions(user_id = user_id)
        groups = groups['groups']['items']
        res = []
        for gr in groups:
            res.append(get_group_description(gr))

    except vk_api.exceptions.ApiError:
        return []
    
def get_user_followers(user_id):
    try:
        followers = vk.users.getFollowers(user_id = user_id)
        return followers['count']
    except vk_api.exceptions.ApiError:
        return 0

def get_user_friends(user_id):
    try:
        friends = vk.friends.get(user_id = user_id)
        return friends['count']
    except vk_api.exceptions.ApiError:
        return 0

def get_group_description(owner_id):
    try:
        group = vk.groups.getById(group_id=owner_id, fields = "description, activity")
        return group[0]['description'] + ' ' + group[0]['activity']
    except vk_api.exceptions.ApiError:
        return "Не указано"


def get_photo_comments(user_id):
    logger.debug("START get_photo_comments")
    processed_photos = []
    processed_comments = []
    user_comments = []
    others_comments = []
    try:
        photos = vk.photos.getAll(owner_id = user_id)
    except vk_api.exceptions.ApiError: 
        return user_comments, others_comments, processed_comments
    logger.debug("Photos size = %s", photos['count'])
    for photo in photos['items'][:10]:
        if photo['id'] not in processed_photos:
            processed_photos.append(photo['id'])
            try:
                comms = vk.photos.getComments(owner_id = user_id, photo_id = photo['id'])
                comms = comms['items']
                logger.debug("Comms size = %s", len(comms))
                for com in comms:
                    if com['id'] not in processed_comments:
                        processed_comments.append(com['id'])
                        if len(com['text']) != 0:
                            if str(com['from_id']) == str(user_id):
                                user_comments.append(com['text'])
                            else:
                                others_comments.append(com['text'])
            except vk_api.exceptions.ApiError: 
                continue
        return user_comments, others_comments, processed_comments
    


def get_all_user_comments(user_id):
    logger.debug("START get_all_user_comments")
    all_comments, others_comments, processed_comments = get_photo_comments(user_id)

    posts, usr_comms, oth_comms = get_user_wall(user_id, processed_comments)
    all_comments.extend(usr_comms)
    others_comments.extend(oth_comms)
    for group in get_user_groups(user_id):
        usr_comms = get_user_in_group_comments(group, user_id)
        all_comments.extend(usr_comms)
    
    return posts, all_comments, others_comments

def get_user_wall(user_id, processed_comments):
    logger.debug("START get_user_wall")
    user_comments = []
    posts = []
    others_comments = []
    wall = None
    try:
        wall = vk.wall.get(owner_id = user_id)
    except vk_api.exceptions.ApiError:
        return posts, user_comments, others_comments
    
    logger.debug("wall size = %s", wall['count'])
    for post in wall['items'][:10]:
        if len(post['text']) != 0:
            posts.append(post['text'])
        if 'copy_history' in post:
            hist = post['copy_history']
                
            if len(hist[0]['text']) != 0:
                #logger.debug("post = %s", hist['text'])
                posts.append(hist[0]['text'])
        try:
            comms = vk.wall.getComments(owner_id = user_id, post_id = post['id'])
            comms = comms['items']
            logger.debug("comms size = %s", len(comms))
            for com in comms:
                if com['id'] not in processed_comments:
                    processed_comments.append(com['id'])
                    if len(com['text']) != 0:
                        if str(com['from_id']) == str(user_id):
                            user_comments.append(com['text'])
                        else:
                            others_comments.append(com['text'])       
        except vk_api.exceptions.ApiError:
            continue
        return posts, user_comments, others_comments
    

def get_user_in_group_comments(owner_id, user_id):
    logger.debug("START get_user_in_group_comments %s", '-' + str(owner_id))

    comments = []
    wall = None
    try:
        wall = vk.wall.get(owner_id = owner_id, count = 10)
    except vk_api.exceptions.ApiError:
        return comments
    for post in wall['items']:
            #print(post['text'])
            #print(post['id'])
        try:
            comms = vk.wall.getComments(owner_id = '-' + str(owner_id), post_id = post['id'])
                #comms = post['comments']
            comms = comms['items']
                #print(comms)
            for com in comms:
                #logger.debug("comm from group %s", com['text'])
                if str(com['from_id']) == str(user_id):
                    comments.append(com['text'])
        except vk_api.exceptions.ApiError:
            continue
    #    logger.debug("BAD")
    #    return comments
    return comments    
    #
    