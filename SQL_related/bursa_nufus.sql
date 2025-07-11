-- Create the table
CREATE TABLE ilce_bursa_nufusu (
    yil INT,
    ilce VARCHAR(50),
    ilce_nufusu INT,
    erkek_nufusu INT,
    kadin_nufusu INT,
    nufus_yuzdesi VARCHAR(10) -- Storing as VARCHAR due to '%' character
);

-- Insert data into the table
INSERT INTO ilce_bursa_nufusu (yil, ilce, ilce_nufusu, erkek_nufusu, kadin_nufusu, nufus_yuzdesi) VALUES
(2024, 'Osmangazi', 885441, 443222, 442219, '% 27,34'),
(2024, 'Yıldırım', 654998, 328669, 326329, '% 20,22'),
(2024, 'Nilüfer', 561730, 277061, 284669, '% 17,34'),
(2024, 'İnegöl', 302251, 152149, 150102, '% 9,33'),
(2024, 'Gemlik', 123361, 62078, 61283, '% 3,81'),
(2024, 'Mudanya', 110797, 53711, 57086, '% 3,42'),
(2024, 'Gürsu', 104867, 53099, 51768, '% 3,24'),
(2024, 'Mustafakemalpaşa', 103581, 51473, 52108, '% 3,20'),
(2024, 'Karacabey', 85968, 42985, 42983, '% 2,65'),
(2024, 'Orhangazi', 82111, 41240, 40871, '% 2,54'),
(2024, 'Kestel', 76659, 38546, 38113, '% 2,37'),
(2024, 'Yenişehir', 55606, 27562, 28044, '% 1,72'),
(2024, 'İznik', 45208, 22290, 22918, '% 1,40'),
(2024, 'Orhaneli', 19069, 9432, 9637, '% 0,59'),
(2024, 'Keles', 11171, 5615, 5556, '% 0,34');