#!/usr/bin/env python3
"""Genera distributors.js (red real de distribuidores Argel) con ciudad normalizada."""
import csv, io, json, re, os

OUT_PATH = os.path.join(os.path.dirname(__file__), "distributors.js")

# Pega aquí la tabla tal cual (TSV): Nombre <tab> Dirección <tab> Teléfono <tab> Lat <tab> Long
DATA = """\
Nombre	Dirección	Teléfono	Lat	Long
AhKimPech Lomas Verdes	Av. Lomas Verdes 414, Los Álamos, 53250 Naucalpan de Juárez, Méx.	+52 56 1031 3311	19.4999932	-99.2508477
AhKimPech Revolución	Av. Revolución 633-Local C y D, San Pedro de los Pinos, Benito Juárez, 03800 Ciudad de México, CDMX	+52 55 6675 1142	19.3859261	-99.1866518
AhKimPech Tlalnepantla	Pte. Sta Mónica 8-Local 203, Las Margaritas, 54050 Tlalnepantla, Méx.	+52 55 9703 6020	19.5262996	-99.2263693
Alpha Depósito Dental	José de San Martín 41, Campestre-Lomas, 31205 Chihuahua, Chih.	+52 614 262 3338	28.6355086	-106.0954843
Armago Deposito Dental	Manuel Doblado 401-A, Tamulté de las Barrancas, 86150 Villahermosa, Tab.	+52 993 351 9905	17.9740101	-92.9564598
Articulos Dentales del Centro	Sitio de Cuautla 206, Hidalgo, 37220 León de los Aldama, Gto.	+52 477 718 4385	21.1454002	-101.6719094
Articulos Dentales del Norte Reynosa	José Ma. Pino Suárez, Centro, 88800 Reynosa, Tamps.	+52 899 930 1985	26.0946238	-98.2848646
Artículos Dentales del Norte	C. Ruperto Martínez Ote. 923, Centro, 64000 Monterrey, N.L.	+52 81 8375 1229	25.6763306	-100.3060832
BIGtree Tu Depósito Dental	Av. Adolfo López Mateos Sur 4186-Int 9, La Giralda, 45088 Zapopan, Jal.	+52 33 3361 8587	20.6446856	-103.4061858
Bodega Dental Del Sol	C. Pedro Moreno 1585, Col Americana, 44160 Guadalajara, Jal.	+52 33 3826 9360	20.6751538	-103.3702441
Bodeguita Dental	Blvd. Agua Caliente 8470, Zona Centro, 22000 Tijuana, B.C.	+52 664 524 5958	32.523468	-117.0318707
Bodeguita Dental Mexicali	Calz Independencia 1976-Int 1, Calafia, 21040 Mexicali, B.C.	+52 686 349 9551	32.63572	-115.454252
Burgos Deposito Dental	Av Central 500, Las Cumbres, 88740 Reynosa, Tamps.	+52 899 920 3984	26.0611581	-98.3328353
Celeste Depósito Dental	Guatemala 382, Tabachines, 36615 Irapuato, Gto.	+52 462 624 7505	20.6942757	-101.3617756
Chicago Dental Puebla	Popocatépetl 2721, Los Volcanes, 72410 Heroica Puebla de Zaragoza, Pue.	+52 222 243 7349	19.0392382	-98.215845
Corporativo Dental Santander	Santander 203, El Dorado 1ra Secc, 20235 Aguascalientes, Ags.	+52 449 913 6398	21.8634493	-102.3084006
Davley Dental	Lic. Adolfo Cano 92, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 314 9285	19.6962879	-101.1777626
DELI Depósito Dental	C/ 15 de Mayo 198 A, La Santa Cruz, 76020 Santiago de Querétaro, Qro.	+52 442 774 5188	20.5979011	-100.3825862
DEN TEC Equipo Técnico y Dental	Av Jacinto Canek 741-Local 2, 97225 Mérida, Yuc.	+52 999 216 5727	20.982113	-89.6510199
Dental Clinic Boutique	Héroe de Nacozari 27, Modelo, 83190 Hermosillo, Son.	+52 662 102 2288	29.1055226	-110.9552433
Dental Cu Ingeniería Dental	Framboyanes 215 Mz M Lt 2, Trinidad de Las Huertas, 68000 Oaxaca de Juárez, Oax.	+52 951 506 0122	17.0495132	-96.7148643
Dental Deposito y Laboratorio Dental	Av Miguel Hidalgo 3820-Local C, Cristóbal Colón, 72330 Heroica Puebla de Zaragoza, Pue.	+52 222 868 6426	19.0461384	-98.1672583
Dental Depot Satélite	Begonias 18 A Sta. Mónica, Cd. Satélite, Tlalnepantla, Méx.	+52 55 5398 4557	19.5286739	-99.2245148
Dental Depot Zacatecas	Av. del Derecho 273, Las Fuentes, 98613 Guadalupe, Zac.	+52 492 224 6296	22.7545695	-102.4982696
Dental Industry Depósito Dental	Gral. Miguel Barragán 129, Centro, 20000 Aguascalientes, Ags.	+52 449 576 3123	21.8849082	-102.2874571
Dental Ink Depósito Dental	Andador 101, Otay Jardín, 22427 Tijuana, B.C.	+52 664 973 1096	32.5295024	-116.9723735
Dental Juquilita	Av. Universidad 216, Trinidad de las Huertas, 68120 Oaxaca de Juárez, Oax.	+52 951 238 7012	17.0507378	-96.7136398
Dental Mix Depósito Dental	Blvd. Fundadores, Col. Cerritos, 25290 Saltillo, Coah.	+52 844 497 3101	25.4285207	-100.9586657
Dental Stock Iztacala	Av. de los Barrios 224, Los Reyes Ixtacala, 54090 Tlalnepantla, Méx.	+52 55 7274 6820	19.5256625	-99.1904893
Dental Store Villahermosa	C. Libertad 116-B, Tamulté de las Barrancas, 86150 Villahermosa, Tab.	+52 993 277 0557	17.9748764	-92.9528051
Dental Supply Reynosa	Allende 150, Centro, 88500 Reynosa, Tamps.	+52 899 258 3333	26.0952237	-98.28248
Dental Universidad Oaxaca	Av. Universidad 500 D, Trinidad de las Huertas, 68120 Oaxaca de Juárez, Oax.	+52 951 506 0798	17.0482924	-96.7141691
Dental USA Products México	Paseo de los Leones 1390-7 Altos, Paseo de Cumbres 1er Sector, 64610 Monterrey, N.L.	+52 81 8020 7506	25.7114397	-100.3771299
Dentales Alfa Villa de Cortés	Calz. de Tlalpan 802 A, Iztaccíhuatl, Benito Juárez, 03520 Ciudad de México, CDMX	+52 55 2165 3585	19.3898697	-99.1383426
Dentalid Depósito Dental	Cda. de Misioneros 2719, San Felipe III Etapa, 31203 Chihuahua, Chih.	+52 614 234 9633	28.6531847	-106.0895481
Dentec Depósito Dental	Av San Felipe 109, San Felipe III Etapa, 31203 Chihuahua, Chih.	+52 614 410 5723	28.6490669	-106.0920626
Dentitodo Depósito Dental	C. Mariano Matamoros 1071, Universidad, 50180 Toluca de Lerdo, Méx.	+52 722 280 5033	19.2733439	-99.6562452
DentixMax Depósito Dental	Blvd. Bernardo Quintana 229, Loma Dorada, 76060 Santiago de Querétaro, Qro.	+52 442 655 9519	20.5975468	-100.3728187
Dentópolis Depósito Dental	Huerto Los Laureles 220, Trinidad de las Huertas, 68120 Oaxaca de Juárez, Oax.	+52 951 506 2210	17.0501262	-96.7144118
Depodent Depósito Dental	Andador Austria esq Dinamarca MzC 54B Local 3, 54700 Cuautitlán Izcalli, Méx.	+52 55 1113 1164	19.6686733	-99.2100152
Depodent Express	Av Teopanzolco 408-Int 3B, Reforma, 62260 Cuernavaca, Mor.	+52 777 682 9408	18.9386684	-99.2226969
Deposito Chicago Dental Oaxaca	Huerto Los Platanares 302, Trinidad de las Huertas, 68120 Oaxaca de Juárez, Oax.	+52 951 144 7381	17.0492476	-96.714221
Deposito Dental 23	C. Cerro de Las Campanas 295, Insurgentes Oeste, 21280 Mexicali, B.C.	+52 686 119 3431	32.6369163	-115.4507962
Deposito Dental Advance	Av. Cuauhtémoc 800-Local 4, 42000 Pachuca de Soto, Hgo.	+52 771 211 7938	20.1207375	-98.7418476
Deposito Dental Aguascalientes	República de Panamá 508, Las Américas, 20230 Aguascalientes, Ags.	+52 449 915 1956	21.8671392	-102.3010134
Deposito Dental Azcapotzalco	Av. Azcapotzalco 786, Los Reyes, Azcapotzalco, 02010 Ciudad de México, CDMX	+52 55 5353 3380	19.4864079	-99.1854305
Deposito Dental Bulldog	Odontología 88, Copilco Universidad, Coyoacán, 04360 Ciudad de México, CDMX	+52 55 2878 7362	19.3360023	-99.1806618
Deposito Dental Cadereyta	Prof. Rosendo Garza 402 Sur, Centro, 67450 Cadereyta Jiménez, N.L.	+52 828 101 9900	25.5885625	-100.0047035
Deposito Dental California	Col. Centro, 22000 Tijuana, B.C.	+52 664 685 4072	32.4972811	-116.9817237
Deposito Dental Centauro	Av Francisco Villa 6305, Panamericana, 31210 Chihuahua, Chih.	+52 614 384 9162	28.6555513	-106.1114262
Deposito Dental Central Bucal	Av. 20 de Noviembre Oriente 155, José Cardel, 91030 Xalapa-Enríquez, Ver.	+52 228 841 3936	19.5361667	-96.9185572
Deposito Dental Chilpancingo	Av. Baja California 210-Int 104, Roma Sur, Cuauhtémoc, 06770 Ciudad de México, CDMX	+52 55 9055 3003	19.4057882	-99.1668484
Deposito Dental Cima	Av. Universidad 285, Lomas del Sol, 37157 León de los Aldama, Gto.	+52 477 311 6244	21.1495774	-101.7093545
Deposito Dental Climaco	J. de La Luz Corral 1911 I, Santo Niño, 31200 Chihuahua, Chih.	+52 614 415 4800	28.6475317	-106.0799503
Deposito Dental Codivas	Lic. Benito Juárez 912, Zona Centro, 25000 Saltillo, Coah.	+52 844 412 3659	25.4177894	-100.9934295
Deposito Dental Cu	Calle Universitarios Ote., Obrero Campesino, 80013 Culiacán Rosales, Sin.	+52 667 729 0872	24.829043	-107.3810559
Deposito Dental Curadent	C. Jesús Carranza 248-A, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 320 2421	19.2737842	-99.6585789
Deposito Dental del Real	Lic. Adolfo Cano 88, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 315 7032	19.6962767	-101.1778843
Deposito Dental del Sureste	Corpus Cristi 20, El Arenal, 68126 Oaxaca de Juárez, Oax.	+52 951 587 3235	17.0450335	-96.7126905
Deposito Dental Del Valle Tlalnepantla	Blvd a Querétaro 13, Viveros del Valle, 54060 Tlalnepantla, Méx.	+52 55 3449 6696	20.5887932	-100.3898881
Deposito Dental Denmart	C. Carrillo Puerto 7184-Local 6, Zona Centro, 22000 Tijuana, B.C.	+52 664 685 1276	32.5332304	-117.0483078
Deposito dental Dent Depot	C. Mariano Matamoros 1063, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 558 7432	19.2743003	-99.6562251
Deposito Dental Dentalmex	Manta 672-Local F, Lindavista, Gustavo A. Madero, 07300 Ciudad de México, CDMX	+52 55 8858 9260	19.4908927	-99.1352331
Deposito Dental Dentco	Guadalupe Victoria 14, Centro, 62000 Cuernavaca, Mor.	+52 777 418 4144	18.9271209	-99.2369526
Deposito Dental el Argentino	Gral. Francisco Villa 209, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 280 7676	19.2737858	-99.655351
Deposito dental Fodent	Gral. Francisco Villa 106, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 919 8324	19.274069	-99.6544168
Deposito Dental Galia	Av. Santa Esther 201 Local 4, Santa Margarita 1a Secc., 45140 Zapopan, Jal.	+52 33 2255 5490	20.727843	-103.4128218
Deposito Dental Gardent	Maestros 239, Panorama, 37160 León de los Aldama, Gto.	+52 477 717 2007	21.1502654	-101.7009116
Deposito Dental Gardent Irapuato	Atilano Nieto 592, Tabachines, 36611 Irapuato, Gto.	+52 462 624 2079	20.6925739	-101.361312
Deposito Dental Gusmart	Av Tecnológico 1302, Bona Gens, 20255 Aguascalientes, Ags.	+52 449 928 9457	21.8780484	-102.2604924
Deposito Dental Gómez Farías CDMX	Congreso 51, Federal, Venustiano Carranza, 15700 Ciudad de México, CDMX	+52 55 3007 6766	19.4176042	-99.0898412
Deposito Dental Gómez Farías Cuernavaca	Av. Cuauhtémoc 119-Loc. 508, Chapultepec, 62450 Cuernavaca, Mor.	+52 777 318 7322	18.920638	-99.2177816
Deposito Dental Gómez Farías Morelia	C. Tte. Cor. José Mª Olvera 171, Nueva Chapultepec, 58280 Morelia, Mich.	+52 443 232 4525	19.6872899	-101.1665516
Deposito Dental Hidalgo	Madrid 204, Andrade, 37020 León de los Aldama, Gto.	+52 477 713 2126	21.1156178	-101.6726981
Deposito Dental Hidalgo Pachuca	Av. Cuauhtémoc 515, Centro, 42040 Pachuca de Soto, Hgo.	+52 771 713 2679	20.1216456	-98.7401258
Deposito Dental Hidalgo Saltillo	Carmen Aguirre de Fuentes 441-3, Zona Centro, 25000 Saltillo, Coah.	+52 844 292 2004	25.4327659	-100.9981571
Deposito Dental Isassi	C. Miguel Hidalgo Ote. 991-L3, Las Quintas, 80060 Culiacán Rosales, Sin.	+52 667 297 1604	24.8099626	-107.3826262
Deposito Dental Iztacala Ar-Dental	Calle Del Encino Mz 12 Cond 4 Casa 29, Los Reyes Ixtacala, 54090 Tlalnepantla, Méx.	+52 55 5461 0132	19.5245508	-99.1919631
Deposito Dental Laguna	Emilio Castelar 932, Zona Centro, 25000 Saltillo, Coah.	+52 844 412 0011	25.4191281	-100.992682
Deposito Dental Leandro Valle	Gómez Farías 5, Centro, 62000 Cuernavaca, Mor.	+52 777 244 3994	18.9279854	-99.2374349
Deposito Dental León	Blvd. San Pedro 704, San Isidro de Jerez, 37510 León de los Aldama, Gto.	+52 477 711 1091	21.0958256	-101.6471672
Deposito Dental Los Bosques	Sierra Nevada 103, Los Bosques, 20120 Aguascalientes, Ags.	+52 449 912 8123	21.9184469	-102.3140544
Deposito Dental Luma	Eduardo Zepeda, Aaron Joaquín, 44768 Guadalajara, Jal.	+52 33 3575 6447	20.6795612	-103.2776738
Deposito dental MADEM	Ignacio Comonfort 2 Bis, Revolución, 91100 Xalapa-Enríquez, Ver.	+52 228 409 9483	19.5702113	-96.9181771
Deposito Dental Madero CLN	Madero 823, Oriente, 80000 Culiacán Rosales, Sin.	+52 667 716 8666	24.8053044	-107.3847476
Deposito Dental Midas	Viad. Javier Rojo Gómez 133, Céspedes, 42090 Pachuca de Soto, Hgo.	+52 771 281 3650	20.1125147	-98.7247466
Deposito Dental Miso	Francisco Márquez 139-Local 1A, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 506 8867	19.6963988	-101.1759374
Deposito Dental Molar	Av. Adolfo Ruiz Cortines 3215, Virginia Cordero de Murillo Vidal, 91017 Xalapa-Enríquez, Ver.	+52 228 282 6992	19.5572135	-96.9326049
Deposito Dental MORELOS	Av. Isidro Olvera 17, Constitución, 83150 Hermosillo, Son.	+52 662 181 9567	29.1039401	-110.9499929
Deposito Dental MT Dental	C. 8va. Miguel Hidalgo 530-L2, Zona Centro, 22000 Tijuana, B.C.	+52 664 868 7182	32.5286806	-117.0290989
Deposito Dental Multident	Dr. Eduardo Aguirre Pequeño 1503-B, Mitras Centro, 64460 Monterrey, N.L.	+52 81 8346 5255	25.6908592	-100.346805
Deposito Dental México	Fray Bartolomé de Las Casas 24-Local 5, Centro, 62000 Cuernavaca, Mor.	+52 777 318 2596	18.9201173	-99.2330119
Deposito Dental Obregón	Calz. Francisco L. Montejano 2095, Calafia, 21040 Mexicali, B.C.	+52 686 556 0706	32.633194	-115.4525815
Deposito Dental Obregón CLN	Prol. Álvaro Obregón 1834, Tierra Blanca, 80030 Culiacán Rosales, Sin.	+52 667 455 3332	24.8248263	-107.396121
Deposito Dental Omega Chihuahua	Av. Benito Juárez 1704, Zona Centro, 31000 Chihuahua, Chih.	+52 614 438 1110	28.6414988	-106.0722821
Deposito Dental Omega CLN	Prol. Álvaro Obregón 1810, Tierra Blanca, 80030 Culiacán Rosales, Sin.	+52 667 147 7940	24.82472	-107.3960175
Deposito Dental Plan de Ayala	Av. Plan de Ayala 601-Planta baja, Vicente Guerrero, 62430 Cuernavaca, Mor.	+52 777 493 0115	18.9243041	-99.2146239
Deposito dental Plazas del Sol	Av. Luis Vega Monrroy 701, Plazas del Sol 1ra Secc, 76099 Santiago de Querétaro, Qro.	+52 442 403 8726	20.5768129	-100.3790788
Deposito Dental Plus Zacatecas	Begonia 1, Centro, 98600 Guadalupe, Zac.	+52 492 149 2482	22.7523226	-102.5245996
Deposito Dental PowerDental	El Campanario 59, El Campanario, 21353 Mexicali, B.C.	+52 686 559 2600	32.6082974	-115.4874905
Deposito Dental Ramos	Calle Hospital 750, Artesanos, 44100 Guadalajara, Jal.	+52 33 3827 3010	20.6851945	-103.3520724
Deposito Dental Reynosa	Aldama 205, Zona Centro, 88500 Reynosa, Tamps.	+52 899 688 3407	26.0957269	-98.2816598
Deposito Dental Saltillo	Blvd. Venustiano Carranza 1638, República, 25280 Saltillo, Coah.	+52 844 413 4402	25.4352761	-100.9945224
Deposito Dental San Pedro	Av. 12 Ote. 605, Barrio de Jesús Tlatempa, 72770 Cholula de Rivadavia, Pue.	+52 222 945 6368	19.0645264	-98.2996471
Deposito Dental Santa Ana	Av. Prol. El Jacal 1050, Puerta Real Residencial, 76910 Santiago de Querétaro, Qro.	+52 442 376 4853	20.557535	-100.4371325
Deposito Dental Santa Anita	S. Antonio 2-A, Lomas del Consuelo, 98614 Guadalupe, Zac.	+52 492 155 0117	22.7549255	-102.5239994
Deposito Dental Santa Fe	Av. Universidad 1103, Bosques del Prado Nte., 20120 Aguascalientes, Ags.	+52 449 146 4030	21.9186245	-102.3142573
Deposito Dental Shalom	Clavel 9, Jardines del Molinito, 53530 Naucalpan de Juárez, Méx.	+52 55 5049 6657	19.4600492	-99.2388651
Deposito Dental SILOH	Carmen Aguirre de Fuentes 619-B, Zona Centro, 25000 Saltillo, Coah.	+52 844 678 8610	25.4332189	-100.9997453
Deposito Dental SOFMAR	Calz. de Los Reyes 22, Jardín Tetela, 62136 Cuernavaca, Mor.	+52 777 984 2956	18.9512899	-99.2488118
Deposito Dental Sonora	Calle Gral. Mariano Escobedo 53, San Benito, 83190 Hermosillo, Son.	+52 662 310 7090	29.0929655	-110.9591742
Deposito Dental SonRyE	Lic. Carlos González Zamora 540, Longoria, 88660 Reynosa, Tamps.	+52 899 925 9088	26.068421	-98.2967947
Deposito Dental Súper Dental	Av Rafael Murillo Vidal 243, Cuauhtémoc, 91060 Xalapa-Enríquez, Ver.	+52 228 690 6387	19.5215822	-96.9067251
Deposito Dental Tecnodent	Lago de Cuitzeo 266, Ventura Puente, 58020 Morelia, Mich.	+52 443 313 4483	19.6928509	-101.191082
Deposito Dental Teopanzolco	Av Teopanzolco 204-Local 12, Teopanzolco, 62350 Cuernavaca, Mor.	+52 777 322 1010	18.9301415	-99.2204547
Deposito Dental Valcro Boulevares	Colina de Buenaventura 45, Boulevares, 53140 Naucalpan de Juárez, Méx.	+52 55 5393 8357	19.4968244	-99.2390733
Deposito Dental Vicefi Saltillo	Av. Universidad 1126, Col. Universidad, Saltillo, Coah.	+52 844 552 0103	25.4445644	-101.001556
Deposito Dental Wendy	Magnolia 13157, Hipódromo Dos, 22195 Tijuana, B.C.	+52 664 904 4514	32.4979194	-116.9826934
Deposito Dental Xola	Calz. de Tlalpan 662, Moderna, Benito Juárez, 03510 Ciudad de México, CDMX	+52 55 5696 1026	19.3948658	-99.137519
Deposito Dental Zapopan	Calle Gómez Farías 301, Linda Vista, 45169 Zapopan, Jal.	+52 33 3633 6611	20.7205412	-103.3946543
Deposito dental Zaye	C. del Llano 242, Lomas del Sol, 37157 León de los Aldama, Gto.	+52 477 141 8125	21.1500685	-101.7107547
Deposito Dentel	Av. Francisco I. Madero 946-Local 1, Segunda, 21100 Mexicali, B.C.	+52 686 552 3822	32.6651641	-115.4790069
Deposito y Unidades Dentales JF	Av. Mariano Otero 5103, Arboledas, 45070 Zapopan, Jal.	+52 33 3632 8030	20.6370387	-103.4207402
Depósito Alvane Dental	Av. del Ahuehuete 107, Jardines de Jerez, 37530 León de los Aldama, Gto.	+52 477 402 9769	21.0901384	-101.649012
Depósito Dental 60	C. 60 346, Plan de Ayala, 97118 Mérida, Yuc.	+52 999 563 3727	21.0151465	-89.6241869
Depósito Dental Acatlán	De Los Tarascos 27, Sta Cruz Acatlán, 53150 Naucalpan de Juárez, Méx.	+52 55 5373 7568	19.4828729	-99.243159
Depósito Dental ADAMS	Av. del Zapatero 108, Industrial Julián de Obregón, 37290 León de los Aldama, Gto.	+52 477 662 7992	21.1042101	-101.6359096
Depósito Dental Alodent	Lic. Adolfo Cano 170-A, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 281 6967	19.6960954	-101.1770493
Depósito Dental ALPADENT	Gral. Francisco Villa 203-C-Pte, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 212 9555	19.2737211	-99.6550387
Depósito Dental ArysDents	2 de Abril 294, Nueva Villahermosa, 86070 Villahermosa, Tab.	+52 914 109 9153	17.9939963	-92.9248597
Depósito Dental Azul	Av. Tlacote 168, Santiago, 76179 Santiago de Querétaro, Qro.	+52 442 349 4693	20.5870753	-100.414796
Depósito Dental BIODENT	La Fragua 348, Barrio de San José, 36500 Irapuato, Gto.	+52 462 173 1296	20.6760643	-101.3429088
Depósito Dental BobaDent	Gral. Francisco Villa 310, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 270 5265	19.2740956	-99.6562052
Depósito Dental Bosques	Andador Austria esq Dinamarca MzC 54B Lt 43 Local 4 PB, 54700 Cuautitlán Izcalli, Méx.	+52 55 5871 7126	19.6686733	-99.2100152
Depósito Dental Bravo	Av. Nicolás Bravo 1631, Inst. Tecnológico de Culiacán, 80220 Culiacán Rosales, Sin.	+52 667 144 2536	24.7881198	-107.4002912
Depósito Dental Calderón	Av. Bosque De Pino Oeste 472, Plutarco Elías Calles, 21376 Mexicali, B.C.	+52 686 843 1107	32.6319528	-115.3853083
Depósito Dental Camfer	Ingenieros 150, Municipio Libre, 20199 Aguascalientes, Ags.	+52 449 186 4261	21.8925564	-102.2620251
Depósito Dental Campestre	Calle 1D x 36 y 38 247, Campestre, 97120 Mérida, Yuc.	+52 999 122 2624	21.0110932	-89.6178717
Depósito Dental Carreto SA de CV	Av. 45 Oriente 1204, Anzures, 72530 Heroica Puebla de Zaragoza, Pue.	+52 222 240 5680	19.0188106	-98.1944426
Depósito Dental Casco de Santo Tomás	Calz de los Gallos 49-Local B, Plutarco Elías Calles, Miguel Hidalgo, 11350 Ciudad de México, CDMX	+52 55 5801 4474	19.456505	-99.1670343
Depósito Dental Chapalita	Av. Tepeyac 1118, Chapalita, 45040 Zapopan, Jal.	+52 33 3122 9127	20.6622176	-103.4054285
Depósito Dental Cipres	Av De Los Barrios Mz 12 Cond 6 Casa 1, Los Reyes Ixtacala, 54090 Tlalnepantla, Méx.	+52 55 5390 4815	19.5226297	-99.1897585
Depósito dental Copident	Salvador Quevedo y Zubieta 220, La Perla, 44360 Guadalajara, Jal.	+52 33 1377 6184	20.6848283	-103.3335548
Depósito Dental Costrudent	Av. Cruz del Sur 4819, Las Águilas, 45080 Zapopan, Jal.	+52 33 3173 0063	20.6288798	-103.4077869
Depósito Dental Couzer Cholula	Av. Miguel Alemán 310, Barrio de Sta María Xixitla, 72760 Cholula de Rivadavia, Pue.	+52 222 636 7885	19.0607272	-98.3077401
Depósito dental del Caribe	Av. Rodrigo Gómez Sm 57 Mz 03 Lt 12-Local 3 y 4, 77533 Cancún, Q.R.	+52 998 267 7548	21.1305031	-86.8319231
Depósito Dental Del Valle Morelia	Fernando Montes de Oca 40, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 427 5790	19.6968576	-101.1758418
Depósito dental Den-things	C. del Deporte 26-A, El Mirador, 54080 Tlalnepantla, Méx.	+52 56 2497 1254	19.5174337	-99.215444
Depósito Dental Dental Depot	C. Citlalli 127, La Colonia, 42185 Pachuca de Soto, Hgo.	+52 771 555 1867	20.0569731	-98.7733948
Depósito Dental DentalCare	Av. Adolfo López Mateos 310, Santiago Tepalcapa, 54743 Cuautitlán Izcalli, Méx.	+52 55 1970 9688	19.6225176	-99.2055926
Depósito Dental DenTec Saltillo	Calle Gral. Carlos Salazar 691, Zona Centro, 25000 Saltillo, Coah.	+52 844 602 3369	25.4192457	-101.0122685
Depósito Dental Dentist Shop	Av. Paseo de Los Bosques 204, Bosques de la Hacienda, 54715 Cuautitlán Izcalli, Méx.	+52 55 9297 0967	19.688301	-99.2185217
Depósito Dental Dento Form	Rosa Venus 114, Molino de Rosas, Álvaro Obregón, 01470 Ciudad de México, CDMX	+52 55 5680 0505	19.3740576	-99.2016398
Depósito Dental Depo-Reb	Manzana 011, Santiago Tepalcapa, 54743 Cuautitlán Izcalli, Méx.	+52 56 1026 6327	19.6239809	-99.2034047
Depósito Dental Difosa	C. Nicolás Bravo 345, Primera, 21100 Mexicali, B.C.	+52 686 516 3470	32.6616661	-115.4843664
Depósito Dental Dmed	Cto. Circunvalación Pte. Mz 009 Lt F-7-Local 23, 53100 Naucalpan de Juárez, Méx.	+52 55 5374 0949	19.5083654	-99.244385
Depósito Dental DOMS	C. 49 570A, Centro, 97000 Mérida, Yuc.	+52 999 928 0317	20.977129	-89.6375811
Depósito Dental Dr Shopping	Av. Xalapa 161, Obrero Campesina, 91020 Xalapa-Enríquez, Ver.	+52 228 202 4240	19.5468035	-96.9287876
Depósito Dental Echegaray	P.º de Echegaray 250-Local 9, Bosques de Echegaray, 53310 Naucalpan de Juárez, Méx.	+52 55 3464 5117	19.4955008	-99.2321324
Depósito Dental El Diente	C. Revolución 300, Centro, 91000 Xalapa-Enríquez, Ver.	+52 228 186 0278	19.5385817	-96.9234141
Depósito Dental Ev San Lorenzo	Av. Tláhuac 38-Local E, San Lorenzo Tezonco, Iztapalapa, 09790 Ciudad de México, CDMX	+52 55 7158 9279	19.3082016	-99.068126
Depósito Dental Express	Av. Chichén Itzá Mz 7 Lt 13 Int A, Supermanzana 27, 77509 Cancún, Q.R.	+52 998 884 9101	21.160299	-86.8484908
Depósito Dental Feregrino	Prol. Pino Suárez 431, Galindas, 76177 Santiago de Querétaro, Qro.	+52 442 215 7053	20.5838345	-100.4150962
Depósito Dental Fernández	Aldama 1100-A1, Centro, 88500 Reynosa, Tamps.	+52 899 925 1096	26.095031	-98.2736388
Depósito Dental Flores	Amanda del Llano 190, Jorge Negrete, Gustavo A. Madero, 07280 Ciudad de México, CDMX	+52 55 5389 9638	19.5300677	-99.1433446
Depósito Dental Fong	Av. Ludwig Van Beethoven 4575, Lomas del Seminario, 45038 Zapopan, Jal.	+52 33 1812 4580	20.6687233	-103.4202296
Depósito Dental Gama	C. Gutemberg 10, Centro, 62000 Cuernavaca, Mor.	+52 777 312 3996	18.9220765	-99.2329863
Depósito Dental GB	Av Paseos del Alba, Edificio J1 Depto 101, Bosques del Alba II, 54750 Cuautitlán Izcalli, Méx.	+52 55 3446 5529	19.6314445	-99.1991402
Depósito Dental Goldentist	Av. Baja California 274-Oficina 451, Hipódromo Condesa, Cuauhtémoc, 06100 Ciudad de México, CDMX	+52 55 8854 7196	19.4056153	-99.1710228
Depósito Dental Guadalupe	Begonias 48-A, Centro, 98600 Guadalupe, Zac.	+52 492 923 4955	22.7533509	-102.5244461
Depósito Dental Guelatao	Batallón de Zacapoaxtla 6-A, Ejército de Oriente Indeco II ISSSTE, Iztapalapa, Ciudad de México, CDMX	+52 55 5745 1248	19.383878	-99.036088
Depósito Dental Hermosillo	Blvd. Juan Navarrete 99-F, Valle Escondido, 83208 Hermosillo, Son.	+52 662 100 5660	29.0858817	-110.9717549
Depósito Dental House	Blvd. Del Vigía 604, El Vigía, 45140 Zapopan, Jal.	+52 33 3905 9924	20.7292111	-103.3946673
Depósito Dental Jalisco Tijuana	Calle Emiliano Zapata 7410, Zona Centro, 22000 Tijuana, B.C.	+52 664 685 2858	32.5312804	-117.0455952
Depósito Dental Junta De Los Ríos	Av. H. Colegio Militar 3102, Junta de los Ríos, 31300 Chihuahua, Chih.	+52 614 174 1856	28.6659133	-106.0758583
Depósito Dental Koj Mérida	Calle 21 102B Local 114-115, Chuburná de Hidalgo, 97205 Mérida, Yuc.	+52 999 195 6413	21.0114393	-89.6325019
Depósito Dental Köh	Cedros 21-Int. E, La Capilla, 76170 Santiago de Querétaro, Qro.	+52 442 215 2999	20.5817881	-100.4099914
Depósito Dental La Cúspide	Blvrd Díaz Ordaz 371, Barrio de San José, 36513 Irapuato, Gto.	+52 462 400 0235	20.6762476	-101.3424422
Depósito Dental La Vía	A. Ferrocarriles Nacionales Pte. 111, Guadalupe, 54805 Cuautitlán, Méx.	+52 55 2139 3691	19.6846737	-99.1831029
Depósito Dental Legaria	Calz Legaria 410-Local 4, Deportivo Pensil, Miguel Hidalgo, 11430 Ciudad de México, CDMX	+52 55 8595 7933	19.450537	-99.2023089
Depósito Dental Ludy	Batallón de Zacapoaxtla 8-A, Ejército de Oriente Indeco II ISSSTE, Iztapalapa, Ciudad de México, CDMX	+52 55 5744 6067	19.3829114	-99.0346831
Depósito Dental LuigiDent Xalapa	Calle Médicos 10, 91017 Xalapa-Enríquez, Ver.	+52 228 843 1507	19.5596376	-96.9287522
Depósito Dental Madental	C. Universitarios 1651, Universitarios, 80030 Culiacán Rosales, Sin.	+52 667 228 3132	24.8288052	-107.3800298
Depósito Dental Madero	Manuel Doblado 222, San Juan de Dios, 37004 León de los Aldama, Gto.	+52 477 716 7540	21.1190476	-101.678302
Depósito Dental Marpad	Pájaro Azul 163, Benito Juárez, 57000 Cdad. Nezahualcóyotl, Méx.	+52 55 2022 0447	19.410689	-99.0185065
Depósito Dental Matamoros	Mariano Matamoros 1065, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 217 2633	19.2741867	-99.656285
Depósito Dental Meridental	Calle 78, Av. Mérida 2000 586, Residencial Pensiones VI, 97217 Mérida, Yuc.	+52 999 987 9970	21.0006234	-89.6643896
Depósito Dental Monterrey	C. Monterrey 314, El Coecillo, 37260 León de los Aldama, Gto.	+52 477 716 4530	21.1214803	-101.6699231
Depósito Dental Morelia	Francisco Márquez 115A, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 189 1866	19.6970625	-101.1759393
Depósito Dental MS Dentec	C. Álamo 27, Valle de Los Pinos 1a. Secc, 54040 Tlalnepantla, Méx.	+52 55 2451 9101	19.5322966	-99.2130338
Depósito Dental MyO	Juan Sebastián Bach 71, Indeco Ánimas, 91190 Xalapa-Enríquez, Ver.	+52 228 812 8514	19.5309183	-96.8890345
Depósito Dental Navarrete	Blvd. Juan Navarrete 89, La Huerta, 83208 Hermosillo, Son.	+52 662 210 4560	29.0858746	-110.9707967
Depósito Dental Odontológica	Av. Paseo Tollocan 500-Pte, Residencial Colón, 50120 Toluca de Lerdo, Méx.	+52 722 917 8823	19.2733114	-99.6587284
Depósito Dental Odontomedic	Calle Miguel Hidalgo 408, José Narciso Rovirosa, 86050 Villahermosa, Tab.	+52 993 233 4613	17.9911875	-92.9351396
Depósito Dental Oro	Aniceto Ortega 1110, Del Valle Sur, Benito Juárez, 03104 Ciudad de México, CDMX	+52 55 5604 0772	19.3726948	-99.166611
Depósito Dental Pleyadent	C.I. M. Altamirano 903-A, Universidad, 50130 Toluca de Lerdo, Méx.	+52 722 219 8529	19.275288	-99.6516273
Depósito Dental Portales	Albert 13, Albert, Benito Juárez, 03560 Ciudad de México, CDMX	+52 55 5672 0200	19.3703246	-99.1407574
Depósito Dental PRO-DENT	Av Jalisco 8, Centro, 83000 Hermosillo, Son.	+52 662 212 0470	29.0846676	-110.9520234
Depósito Dental Providencia	Av. Rubén Darío 1311, Providencia 4a. Secc, 44630 Guadalajara, Jal.	+52 33 1942 8449	20.6966007	-103.3832295
Depósito Dental Punta Norte	Av Géiser 210, El Rocío, 76114 Santiago de Querétaro, Qro.	+52 442 601 2868	20.6201596	-100.4412387
Depósito Dental REISIX	Av. del Taller 535, Jardín Balbuena, Venustiano Carranza, 15900 Ciudad de México, CDMX	+52 55 8854 5976	19.4131822	-99.1094059
Depósito Dental RentaClinic	Av Gabriel Mancera 415, Punta Azul, 42039 Pachuca de Soto, Hgo.	+52 771 129 7021	20.1205598	-98.7818336
Depósito Dental Rivera	Av. Puebla 67, Centro, 83000 Hermosillo, Son.	+52 662 213 2196	29.0851663	-110.9565463
Depósito Dental Román	C. Río Verde 7, El Molinito, 53530 Naucalpan de Juárez, Méx.	+52 56 2589 2564	19.4595087	-99.2374997
Depósito Dental RulyDent	C. 19 194, Miraflores, 97179 Mérida, Yuc.	+52 999 923 0878	20.956379	-89.5970626
Depósito Dental Río Lab	Misión de San Diego 1527-Int. 103, Zona Urbana Río Tijuana, 22010 Tijuana, B.C.	+52 664 201 5434	32.5186958	-117.0111057
Depósito Dental San Javier	Plaza de Las Américas Local 20-A, Valle de San Javier, 42086 Pachuca de Soto, Hgo.	+52 771 719 2815	20.0969745	-98.7522469
Depósito Dental San Javier 200	Blvd. Valle de San Javier 200, Valle de San Javier, 42086 Pachuca de Soto, Hgo.	+52 771 279 7273	20.10059	-98.751693
Depósito Dental Santa Lucía	Arco Vespaciano 1114 A, Arcos de Zapopan, 45130 Zapopan, Jal.	+52 33 1972 5173	20.7404594	-103.4099517
Depósito Dental Santo Niño	C. 27 Manuel Gómez Morín 1318, Santo Niño, 31200 Chihuahua, Chih.	+52 614 201 9130	28.6501747	-106.0782009
Depósito Dental Siglo 21	Calz. de Tlalpan 754, Iztaccíhuatl, Benito Juárez, 03520 Ciudad de México, CDMX	+52 55 5696 3413	19.3914889	-99.1379964
Depósito Dental Siglo XXI	Calle Gral. Manuel Pérez Treviño 725, Zona Centro, 25000 Saltillo, Coah.	+52 844 453 9854	25.4269187	-101.0056197
Depósito Dental SIMAO	Paseo del Estudiante 100, PRI Chacón, 42186 Pachuca de Soto, Hgo.	+52 55 4919 4348	20.0857662	-98.7411839
Depósito Dental SOS	Rayón 1009, Trinidad de las Huertas, 68115 Oaxaca de Juárez, Oax.	+52 951 466 2017	17.0563338	-96.7154461
Depósito Dental Stanford Irapuato	Guatemala 463-B, Tabachines, 36615 Irapuato, Gto.	+52 462 215 6335	20.6945999	-101.3611212
Depósito Dental Tech	Av Francisco Zarco 4, Constitución, 83150 Hermosillo, Son.	+52 662 367 6321	29.1020095	-110.9527212
Depósito Dental Unidos Hermosillo	Blvd. José María Morelos y Pavón 755-D, Cumbres Residencial, 83143 Hermosillo, Son.	+52 662 284 7880	29.1380776	-110.9527462
Depósito Dental Universidad	C. Escorza 559, Col Americana, 44160 Guadalajara, Jal.	+52 33 1863 5160	20.6680237	-103.3582994
Depósito Dental Unión Zacatecas	S. Rafael 69 B, Centro, Guadalupe, Zac.	+52 492 491 0765	22.7528803	-102.5235095
Depósito Dental Valladolid	Fernando Montes de Oca 160, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 260 7125	19.6965625	-101.1745681
Depósito Dental Vasco de Quiroga	Lic. Adolfo Cano 200, Chapultepec Nte., 58260 Morelia, Mich.	+52 443 690 7741	19.6961576	-101.1768489
Depósito Dental Vedent CLN	Citlaltépec 2924, Rincón del Humaya, 80058 Culiacán Rosales, Sin.	+52 667 309 8416	24.821651	-107.4291059
Depósito Dental Veintiuno	Av. Sirak Baloyan 1901, Zona Centro, 22000 Tijuana, B.C.	+52 664 290 0265	32.5254589	-117.0296709
Depósito Dental Viaducto	C. Niceto de Zamacois 82, Iztacalco, 08200 Ciudad de México, CDMX	+52 55 5440 1525	19.4003235	-99.1359953
Depósito Dental Villa de Cortés	Calz. de Tlalpan 836, Villa de Cortés, Benito Juárez, 03530 Ciudad de México, CDMX	+52 55 5698 0060	19.3887038	-99.1384236
Depósito Dental Yanim Cancún	Mz 8 Lt 8 11, Las Playas 29, 77508 Cancún, Q.R.	+52 998 401 1873	21.158835	-86.8409414
Depósito Dental Zacatecas	Av. Insurgentes 226, Zacatecas Centro, 98000 Zacatecas, Zac.	+52 492 688 2659	22.7677227	-102.5743076
Depósito Dental Zuma	Manzana 032, Ejido el Socorro, 54714 Cuautitlán Izcalli, Méx.	+52 55 8201 6781	19.6840641	-99.1848868
Depósito Dental Zuthman	Hortaliza 3-Local 5, Loma Bonita, 76048 Santiago de Querétaro, Qro.	+52 442 749 1333	20.587902	-100.3676435
Depósito Dentalmedic Store	C. Zumpango 112, La Romana, 54030 Tlalnepantla, Méx.	+52 55 5390 8742	19.5437144	-99.1904051
Depósito Mercadito Dental	Joaquín Clausel 2226-Int A3 Piso 1, Zona Urbana Río Tijuana, 22010 Tijuana, B.C.	+52 664 709 8224	32.5234293	-117.0169038
Depósito Mundo Dental Oaxaca	Sabinos 501-A, Reforma, 68050 Oaxaca de Juárez, Oax.	+52 951 524 7322	17.0773611	-96.7134836
Depósito Nova Dental	López Portillo 807, La Perla, 44360 Guadalajara, Jal.	+52 33 1329 3246	20.6851505	-103.3338922
Depósito Omega Dental	C. Siete Colinas 1487, Independencia, 44290 Guadalajara, Jal.	+52 33 3651 3142	20.6991403	-103.330544
Depósito Universo Dental	Av de los Árboles 625, Tulipanes II, 42185 Pachuca de Soto, Hgo.	+52 771 420 4195	20.0604571	-98.7697069
Depósito Willy Dental	Teodoro Lavoignet 2, Rafael Murillo Vidal, 91000 Xalapa-Enríquez, Ver.	+52 228 814 8667	19.5277231	-96.9167306
DGM Material Dental	Dr. Eduardo Aguirre Pequeño 909, Mitras Centro, 64460 Monterrey, N.L.	+52 81 1198 3752	25.6929931	-100.3466192
Diseño Dental Querétaro	Av Tecnológico 2-Local 208, Centro, 76000 Santiago de Querétaro, Qro.	+52 442 215 2393	20.5878121	-100.4040805
Distribuidora Dental Guadalajara	C. José María Echauri 183A, La Perla, 44360 Guadalajara, Jal.	+52 33 3618 2514	20.6851102	-103.3341453
Distribuidora Dental MAREG	Blvd. Miguel Hidalgo 330-Local 10, Bella Vista, 88600 Reynosa, Tamps.	+52 899 120 3380	26.0866276	-98.2876411
Distribuidora Dental Satélite	Cto Héroes 41-Local D, Cd. Satélite, 53100 Naucalpan de Juárez, Méx.	+52 55 2155 4981	19.5042646	-99.2314971
Distribuidora Dental Stanford	Sierra Fría 121, Bosques del Prado Nte., 20127 Aguascalientes, Ags.	+52 449 200 2009	21.9177016	-102.3128579
DM Depósito Dental Villahermosa	Miguel Hidalgo 236 B, Centro, 86000 Villahermosa, Tab.	+52 993 314 3967	17.9899873	-92.9204727
El Depósito Dental Premium	Calz de los Gallos 27-2, Plutarco Elías Calles, Miguel Hidalgo, 11350 Ciudad de México, CDMX	+52 55 6821 4084	19.4563811	-99.1660961
Emporio Dental Deposito	Calz. de la República, Jalatlaco 715 altos, Centro, 68000 Oaxaca de Juárez, Oax.	+52 442 194 2937	17.0689427	-96.7180429
Equipos Dentales Oaxaca	Huerto Los Framboyanes 407, Trinidad de las Huertas, 68120 Oaxaca de Juárez, Oax.	+52 951 144 7755	17.0493921	-96.7140763
Eurodental SA de CV	Av 27 Pte 1503-Planta Baja, Los Volcanes, 72410 Heroica Puebla de Zaragoza, Pue.	+52 222 912 2204	19.0400483	-98.2154999
Gilsamedic Depósito Dental	Priv. de la 5 Sur 3101-Local 1, Chulavista, 72420 Heroica Puebla de Zaragoza, Pue.	+52 222 276 9468	19.034516	-98.2094889
Ideas Dentales	Sta. Margarita 515, Insurgentes San Borja, Benito Juárez, 03100 Ciudad de México, CDMX	+52 55 1136 2032	19.3819967	-99.1757276
Imadental Deposito Dental	Av. Minas Palacio 8, San Antonio Zomeyucan, 53570 Naucalpan de Juárez, Méx.	+52 55 2452 8643	19.4581804	-99.2385516
Izcadent Depósito Dental	P.º del Bosque Mz 51 Lt 2, Bosques de Morelos, 54760 Cuautitlán Izcalli, Méx.	+52 55 5881 9143	19.6308795	-99.2295827
Jama Dental Médico	Celaya 3126, Mitras Centro, 64460 Monterrey, N.L.	+52 81 8346 1313	25.6900128	-100.3466567
Keiko Deposito Dental	Huexotitla, 72534 Heroica Puebla de Zaragoza, Pue.	+52 222 243 3253	19.0272478	-98.2107037
Kelca Dent Deposito Dental	Palenque Sm 29 Mz 1 Lt 9, 77508 Cancún, Q.R.	+52 998 235 5214	21.1622604	-86.8390767
La Casa del Dentista	Annapurna 2001-A, Solidaridad, 80058 Culiacán Rosales, Sin.	+52 667 175 2952	24.820522	-107.4270206
Libra Grupo Dental	Av. de los Barrios Mz 13 Lt 1-Casa 8, Los Reyes Ixtacala, 54090 Tlalnepantla, Méx.	+52 55 6648 2335	19.5226297	-99.1897585
Line Orthodoc	Ébano 702 B, Circunvalación Nte., 20020 Aguascalientes, Ags.	+52 449 153 1521	21.903184	-102.3006241
Marduk Depósito Dental	Salvador Quevedo y Zubieta 406, Independencia Oriente, 44340 Guadalajara, Jal.	+52 33 1202 0624	20.6839125	-103.3325053
Mark Inc Deposito Dental	Av. 33 Pte. 1319, Los Volcanes, 72410 Heroica Puebla de Zaragoza, Pue.	+52 222 496 1030	19.0368207	-98.2160424
MDC Dental	Industria del Plástico 2113, Zapopan Industrial Nte., 45130 Zapopan, Jal.	+52 800 363 7800	20.7421606	-103.3897373
Movident Xalapa	Av. Adolfo Ruiz Cortines 1602, Tamborrel, 91050 Xalapa-Enríquez, Ver.	+52 228 112 6619	19.5363395	-96.9329129
Odontec Culiacán	Rodolfo G. Robles 693-Pte, Colonia Centro, 80000 Culiacán Rosales, Sin.	+52 667 348 8697	24.7999634	-107.4011727
Odontotec Deposito Dental	C. Chopo 43, Villas del Descanso, 62554 Jiutepec, Mor.	+52 777 319 0696	18.8940332	-99.1673268
Odovent Depósito Dental	Calz. de las Américas 1002-Local F, Sonora, 21210 Mexicali, B.C.	+52 686 372 3833	32.6632544	-115.4309975
Orion Depósito Dental	Av. Luis Donaldo Colosio Murrieta 158, El Centenario, 83260 Hermosillo, Son.	+52 662 212 7030	29.079938	-110.9630744
ORTHOMEX Depósito Dental	Calz. Francisco L. Montejano 1771, Calafia, 21040 Mexicali, B.C.	+52 686 309 1207	32.6289826	-115.4525261
Orthorey	Av. Prof. Moisés Sáenz 1100, Mitras Centro, 64600 Monterrey, N.L.	+52 81 8348 6869	25.6943038	-100.347256
Pro Dent Deposito Dental	Av San Antonio Mz 5 Lt 13-Local 2, Santa Rosa de Lima, 54740 Cuautitlán Izcalli, Méx.	+52 55 5868 4405	19.6608675	-99.2207813
Prodechisa Depósito Dental	Av. Glandorf 3106-A, San Felipe I Etapa, 31203 Chihuahua, Chih.	+52 614 688 7792	28.650075	-106.093312
Prodental Depósito Dental Saltillo	Emilio Castelar 696-A, Zona Centro, 25000 Saltillo, Coah.	+52 844 879 9020	25.4199478	-100.994547
Prodental Depósito Dental Toluca	Av. de los Maestros 606-Local 3, Doctores, 50060 Toluca de Lerdo, Méx.	+52 722 215 2222	19.295896	-99.6443957
Prodonsa	Celaya 105, Mitras Centro, 64460 Monterrey, N.L.	+52 81 8333 4486	25.690077	-100.3447077
Productos Dentales Monterrey	Emilio Carranza 123 Sur, Centro, 64000 Monterrey, N.L.	+52 81 8343 0277	25.6754867	-100.3115946
Productos Dentales Tovar	Playa Revolcadero 212, Reforma Iztaccíhuatl Nte., Iztacalco, 08810 Ciudad de México, CDMX	+52 55 5696 0912	19.3905456	-99.1310226
Promadent Deposito Dental	C. 59 544, Parque Santiago, Centro, 97000 Mérida, Yuc.	+52 999 264 7486	20.9693297	-89.627684
Promadent Villahermosa	Calle Andrés Sánchez Magallanes 903, Centro Delegación Seis, 86000 Villahermosa, Tab.	+52 993 312 9914	17.9947732	-92.9218285
Promovago Reynosa	Gómez Farías 770, Col del Prado, 88560 Reynosa, Tamps.	+52 899 922 7709	26.0895918	-98.2693226
Recodi Dental	Rufino Blanco Fombona 2504, Iztaccíhuatl, Benito Juárez, 03520 Ciudad de México, CDMX	+52 55 5784 9998	19.3906257	-99.1381049
Saacri Depósito Dental	Montes Himalaya 827, Jardines de la Concepción II, 20120 Aguascalientes, Ags.	+52 449 251 0050	21.9228822	-102.2988981
SmartDent Las Fuentes	Blvrd del Maestro 377-Local 1C, Las Fuentes Secc Aztlán, 88710 Reynosa, Tamps.	+52 899 199 0180	26.0700392	-98.3215292
Student Depósito Dental	Riva Palacio 2108, Santo Niño, 31200 Chihuahua, Chih.	+52 614 341 0068	28.6494379	-106.080758
Todo Dental	Dr. Eduardo Aguirre Pequeño 905, Mitras Centro, 64460 Monterrey, N.L.	+52 81 1772 6845	25.6928766	-100.3466047
Todo Dental Naucalpan	Av. Vía Adolfo López Mateos 201, Sta Cruz Acatlán, 53150 Naucalpan de Juárez, Méx.	+52 55 4236 5590	19.4815294	-99.2506329
Tooth and Tools BUAP	Popocatépetl 2737, Los Volcanes, 72410 Heroica Puebla de Zaragoza, Pue.	+52 221 570 1168	19.0386053	-98.2162659
Tutti Dental SA de CV	Odontología 75, Copilco Universidad, Coyoacán, 04360 Ciudad de México, CDMX	+52 55 5658 9372	19.3355063	-99.1805752
Tuzo Dental Deposito Dental	Blvrd Luis Donaldo Colosio 2003, Coscotitlán, 42064 Pachuca de Soto, Hgo.	+52 771 719 6510	20.0913788	-98.7542493
Ugaldent Depósito Dental	Av. Profra. Carmen Rivera 52, Profesores Estatales, 21280 Mexicali, B.C.	+52 686 566 3099	32.6343092	-115.4514575
Universum Dental	Av. Mérida 2000, Residencial Pensiones VI, 97217 Mérida, Yuc.	+52 999 316 5658	20.9996387	-89.6642505
Vacnor Depósito Dental	C. Pípila 47, Col. Centro, 36500 Irapuato, Gto.	+52 462 627 7940	20.6714642	-101.3474361
Vital Dental Cancún	Av. Palenque esq. Camarón Mz 4 Lt 1, 77509 Cancún, Q.R.	+52 998 898 3374	21.1616356	-86.8388617
Zenith Deposito Dental y Médico	Carretera a Cholul, Calle 7, Santa Rita Cholul, 97305 Mérida, Yuc.	+52 999 688 3901	21.0290788	-89.5694924
Zenith Depósito Dental en Cancún	Alcatraces Sm 22 Mz 13 Lt 63, 77500 Cancún, Q.R.	+52 998 221 6478	21.1605096	-86.8271798
"""

# Normaliza nombres oficiales largos a la ciudad de uso común (para el selector manual).
CITY_NORMALIZE = {
    "Heroica Puebla de Zaragoza": "Puebla",
    "Santiago de Querétaro": "Querétaro",
    "León de los Aldama": "León",
    "Culiacán Rosales": "Culiacán",
    "Cholula de Rivadavia": "Cholula",
    "Xalapa-Enríquez": "Xalapa",
    "Toluca de Lerdo": "Toluca",
    "Oaxaca de Juárez": "Oaxaca",
    "Cdad. Nezahualcóyotl": "Nezahualcóyotl",
    "Pachuca de Soto": "Pachuca",
    "Cadereyta Jiménez": "Cadereyta",
    "Naucalpan de Juárez": "Naucalpan",
}


def city_of(addr):
    parts = [p.strip() for p in addr.split(",") if p.strip()]
    if len(parts) >= 2:
        pen = re.sub(r"^\d{4,5}\s*", "", parts[-2]).strip()
    elif parts:
        pen = parts[-1]
    else:
        pen = ""
    return CITY_NORMALIZE.get(pen, pen)


rows = list(csv.reader(io.StringIO(DATA), delimiter="\t"))
header = rows[0]
out = []
for i, r in enumerate(rows[1:], start=1):
    if len(r) < 5 or not r[0].strip():
        continue
    name, addr, phone, lat, lng = r[0], r[1], r[2], r[3], r[4]
    out.append({
        "id": f"d{i}",
        "name": name.strip(),
        "addr": addr.strip(),
        "phone": phone.strip(),
        "city": city_of(addr),
        "lat": round(float(lat), 6),
        "lng": round(float(lng), 6),
    })

cities = sorted({d["city"] for d in out if d["city"]})
js = (
    "// Generado automáticamente desde build_distributors.py — no editar a mano.\n"
    "const DISTRIBUTORS = " + json.dumps(out, ensure_ascii=False, indent=0) + ";\n"
    "const DIST_CITIES = " + json.dumps(cities, ensure_ascii=False) + ";\n"
)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(js)

print(f"{len(out)} distribuidores, {len(cities)} ciudades -> {OUT_PATH}")
print("Ciudades:", ", ".join(cities))
