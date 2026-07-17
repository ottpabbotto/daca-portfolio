Eeldused:

    Keskmine kogukäive koos ja ilma miinustes klientidega:

    | üldine_keskmine_kogukaive | puhastatud_keskmine_kogukaive |
    | ------------------------- | ----------------------------- |
    | 832.61                    | 843.43                        |

    VIP klientideks määratud kliendid, kelle keskmine käive ületab 800 eurot.

Vastused:

   - Mitu klienti on igas segmendis (VIP, Regular, Uus)?

    | segment | klientide_arv |
    | ------- | ------------- |
    | VIP     | 1228          |
    | Regular | 1208          |
    | Uus     | 684           |
    | ?       | 30            |

   - Mis on iga segmendi keskmine käive?

    | segment | klientide_arv | keskmine_kaive_kliendi_kohta |
    | ------- | ------------- | ---------------------------- |
    | VIP     | 1228          | 1702.61                      |
    | Regular | 1208          | 443.71                       |
    | Uus     | 684           | 6.87                         |
    | ?       | 30            | -292.38                      |

   - Millistes linnades on kõige rohkem VIP-kliente?
   
    | city       | vip_klientide_arv |
    | ---------- | ----------------- |
    | Tallinn    | 491               |
    | Tartu      | 250               |
    | Pärnu      | 138               |
    | Narva      | 63                |
    | Rakvere    | 44                |
    | Viljandi   | 42                |
    | Kuressaare | 40                |
    | Haapsalu   | 39                |
    | Jõhvi      | 33                |
    | Valga      | 32                |
    | Võru       | 30                |
    | Paide      | 26                |

Soovitused:

    - Välja uurida, miks on 30 kliendi tehingud miinuses.
    - Hinnata ümber VIP klientide jaotus

    | kogukaive_vahemik | klientide_arv |
    | ----------------- | ------------- |
    | üle 20000         | 11            |
    | 10001 - 20000     | 5             |
    | 5001 - 10000      | 4             |
    | kuni 5000         | 1209          |

    | top_11_kogukaive_kokku |
    | ---------------------- |
    | 514782.99              |
    