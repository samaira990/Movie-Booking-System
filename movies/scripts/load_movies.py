import random
from datetime import date, timedelta
from movies.models import Movie, Genre, Language


WORDS = [
    "Shadow", "Rise", "Legend", "Mission", "Empire",
    "Storm", "Dragon", "Code", "Matrix", "Journey",
    "War", "Secret", "Night", "Fire", "Sky",
    "Echo", "Blade", "King", "Queen"
]

GENRE_POSTERS = {
    "Action": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734357/kid-circus-7vSlK_9gHWA-unsplash_gyc0ms.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734332/ethan-elisara-9VRlK7lu1Ck-unsplash_i0n0gc.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734318/tom-morbey-r1SwcagHVG0-unsplash_k1k424.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734302/jonathan-francis-U1OdQbMi6ys-unsplash_nizudz.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734282/kamil-pietrzak-OSfCunpfKsE-unsplash_szsqj2.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734264/patrick-fore-YueS9MGF4Lo-unsplash_posdda.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734523/sean-benesh-6Nbo9Pn0yJA-unsplash_fqxqo2.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733028/1amfcs-_UTH788EaRg-unsplash_ra9lqj.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733013/jakob-owens-IqjrtWEzMIg-unsplash_rb3hom.jpg",

    ],

    "Thriller": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734067/edilson-borges-GSrgTVqS0dk-unsplash_wie4fq.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734049/johannes-plenio-BvSObUWmOVw-unsplash_scu7ez.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734034/mikolaj-zeman-yANpMjyQEvs-unsplash_tig5yd.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733998/chris-grafton-MRqzGrboQYI-unsplash_f12nxk.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733292/johnny-kulula-y8mbY2uFDQU-unsplash_glbl5n.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733277/jason-leung-44S2NSkJ_gc-unsplash_ywyauq.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733267/bruno-guerrero-QPsJnGZw4P4-unsplash_focvf5.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779733248/pexels-markus-winkler-1430818-18524145_a2ghr4.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734134/paolo-d-andrea-esYZII6LF_w-unsplash_gk5jtc.jpg",

    ],

    "Sci-Fi": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734379/8machine-_-LhNDEs4MP5w-unsplash_z8isss.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734400/tim-van-der-kuip-ZGKqdnfbOWo-unsplash_ommlov.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734420/nathan-duck-KnLj3o9A66E-unsplash_phrhwp.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734459/mike-uderevsky--fW75WfpAfc-unsplash_a7xzm3.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734476/zoltan-tasi-jfanHOkBEkw-unsplash_fmm0hw.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734492/cash-macanaya-XDFfAHlxw9I-unsplash_a3bd2d.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734509/matthieu-buhler-WnfKYqxWH8Q-unsplash_iuutu3.jpg",

    ],

    "Drama": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736628/pexels-manishjangid-36470383_gqeld9.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736586/pexels-kosyginl-28993930_ubstt8.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736576/pexels-vijay-richhiya-2155208704-36430688_msudvz.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734134/paolo-d-andrea-esYZII6LF_w-unsplash_gk5jtc.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734120/danie-franco-f49XhYbpiA0-unsplash_ziujfv.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734105/ali-nejatian-D3KYmPveqsw-unsplash_qnd3xz.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734093/resat-kuleli-D-gXsGHyuv8-unsplash_aawydo.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734078/kirill-balobanov-2rIs8OH5ng0-unsplash_xfvgvt.jpg",

    ],

    "Comedy": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734586/0xk-cV2DN3viNIM-unsplash_xok7aj.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734565/louis-hansel-rCbl7pLTy90-unsplash_yymfs7.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734540/pandhuya-niking-opaBTJV25Ks-unsplash_tfdlgu.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734253/tim-mossholder-imlD5dbcLM4-unsplash_y7v47e.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734234/call-me-fred-969TUssR2S4-unsplash_kazplx.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734215/michel-grolet-NBRNK4XC1k8-unsplash_mw8rdw.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734198/steve-harrris-aTuAKskNy7Y-unsplash_a4ih1k.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734183/kevin-snow-KFrR77keJRQ-unsplash_aba6my.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779734152/marija-zaric-q73jLftKN-A-unsplash_dtpci5.jpg",

    ],

    "Mythological": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736884/the-cleveland-museum-of-art-ygiugDk-KQY-unsplash_uvvuxy.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736870/the-cleveland-museum-of-art-J1yxoDMCJlc-unsplash_epiorn.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736815/rashni-parichha-4HtfBcrqtDI-unsplash_x0jvxj.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736758/piyush-modi-7waKZcRjylc-unsplash_ixgmg6.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736742/mohnish-landge-Q9GBNYnAiHM-unsplash_jzgq1y.jpg",
        ""

    ],

    "History": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736344/pexels-bulat843-1243575272-28571816_fzbvre.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736325/pexels-sachin-shettigar-1251682-34962792_zvuvcb.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736314/pexels-vineeth-unni-174296001-31356592_xpuq4h.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736644/pexels-rahul-patil-423932438-15867003_noaqpd.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736673/pexels-mugesh-dsraj-218642671-11885732_wburvr.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736688/pexels-vishvajeet-kumar-1546875-36340656_req1k8.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736720/pexels-sunil-97165465-15259942_pktfwn.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736586/pexels-kosyginl-28993930_ubstt8.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736606/pexels-143deepak-14069974_o8uojt.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736576/pexels-vijay-richhiya-2155208704-36430688_msudvz.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736628/pexels-manishjangid-36470383_gqeld9.jpg",



    ],

    "Patriotic": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736538/prakhar-sharma-oNo8uJgUgD0-unsplash_izrvby.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736548/pexels-yl-lew-88954986-35755249_cia3rm.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736562/yaed-0wxeci_r360-unsplash_cvfbyv.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736576/pexels-vijay-richhiya-2155208704-36430688_msudvz.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736606/pexels-143deepak-14069974_o8uojt.jpg",

    ],

    "Devotional": [
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736354/pexels-plato-terentev-3804555-5910148_aelbx4.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736365/pexels-nishantaneja-2385606_xxv44p.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736521/pexels-artosuraj-28819289_gtlhon.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736453/pexels-dvineyoga-4340795_xzj3ps.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736397/pexels-yoga-course-india-932671557-20035472_mqpg4q.jpg",
        "https://res.cloudinary.com/dnn5jpypb/image/upload/q_auto/f_auto/v1779736506/pexels-pawan-sable-255075564-13718529_ouiqzg.jpg",


    ],
}


# -----------------------------------
# CAST + DESCRIPTIONS
# -----------------------------------
CAST_NAMES = [
    "Actor A",
    "Actor B",
    "Actor C",
    "Actor D",
    "Actor E",
    "Actor F",
    "Actor G",
]

DESCRIPTIONS = [
    "An explosive action-packed journey where courage, sacrifice, and destiny collide in an unforgettable battle.",

    "A gripping thriller filled with suspense, hidden secrets, and unexpected twists that keep you guessing.",

    "A futuristic sci-fi adventure exploring advanced technology, unknown worlds, and humanity's ultimate fate.",

    "An emotional drama about love, loss, relationships, and the choices that define our lives.",

    "A light-hearted comedy packed with laughter, chaos, and unforgettable moments of pure entertainment.",

    "A grand mythology epic inspired by ancient legends, divine powers, and timeless battles between good and evil.",

    "A historical journey through India’s glorious past, showcasing legendary rulers, great battles, and cultural heritage.",

    "A patriotic story celebrating bravery, sacrifice, and unwavering love for the nation.",

    "A spiritual journey of self-discovery, faith, devotion, and inner peace.",

    "An intense tale of heroism where one person rises against impossible odds to change destiny forever.",

    "A mysterious adventure where hidden truths slowly unfold, revealing shocking secrets.",

    "A powerful story of friendship, loyalty, and resilience through life’s greatest challenges.",

    "A breathtaking cinematic experience filled with emotion, action, and unforgettable moments.",

    "An inspiring journey where ordinary people discover extraordinary strength within themselves.",

    "A captivating story blending suspense, emotion, and excitement into an unforgettable experience.",
]


# -----------------------------------
# HELPERS
# -----------------------------------
def random_title():
    return f"{random.choice(WORDS)} {random.choice(WORDS)}"


def random_date():
    start = date(2015, 1, 1)
    end = date(2025, 12, 31)
    delta = end - start

    return start + timedelta(
        days=random.randint(0, delta.days)
    )


def random_poster(selected_genres):
    genre_names = [g.name for g in selected_genres]

    for genre in genre_names:
        if genre in GENRE_POSTERS:
            return random.choice(
                GENRE_POSTERS[genre]
            )

    return random.choice(
        GENRE_POSTERS["Action"]
    )


# -----------------------------------
# MAIN SEED FUNCTION
# -----------------------------------
def run():
    genres = list(Genre.objects.all())
    languages = list(Language.objects.all())

    if not genres or not languages:
        print("❌ Add genres and languages first.")
        return

    print("Creating 5000 movies...")

    movie_data = []
    relation_data = []

    for i in range(5000):
        selected_genres = random.sample(
            genres,
            k=random.randint(1, 3)
        )

        selected_languages = random.sample(
            languages,
            k=random.randint(1, 2)
        )

        movie = Movie(
            name=f"{random_title()} {i}",
            image=random_poster(selected_genres),
            rating=round(
                random.uniform(5.0, 9.5),
                1
            ),
            cast=", ".join(
                random.sample(CAST_NAMES, 3)
            ),
            description=random.choice(
                DESCRIPTIONS
            ),
            release_date=random_date(),
        )

        movie_data.append(movie)

        relation_data.append(
            (
                selected_genres,
                selected_languages
            )
        )

    # Fast insert
    Movie.objects.bulk_create(
        movie_data,
        batch_size=500
    )

    print("Assigning genres and languages...")

    created_movies = list(
        Movie.objects.order_by("-id")[:5000]
    )

    for movie, relations in zip(
        created_movies,
        relation_data
    ):
        selected_genres, selected_languages = relations

        movie.genres.set(
            selected_genres
        )

        movie.languages.set(
            selected_languages
        )

    print("✅ 5000 movies created successfully!")