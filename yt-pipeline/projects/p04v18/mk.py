import json
L = "GASPARÍN · 1945"
S = [
 dict(src=["CC@30-380", "BM@40-390"], label=L, cap="",
      txt="Seguro conoces a Gasparín, el fantasma amigable, ese fantasmita blanco que solo quería hacer amigos. Parece la caricatura más tierna del mundo. Pero detrás de Gasparín hay una pelea entre dos creadores, una venta de ciento setenta y cinco dólares, un primer episodio sorprendentemente oscuro y hasta una nave espacial que viajó a la Luna con su nombre."),
 dict(src=["FG@200-540", "GB@60-510"], label=L, cap="10 DATOS INCREÍBLES",
      txt="Hoy te cuento diez datos increíbles sobre Gasparín, el personaje que Paramount llevó a los cines en 1945, y que después conquistó los cómics, la televisión y hasta el cine con efectos por computadora. Algunos de estos datos te van a cambiar la forma de ver al fantasma más amigable de la animación. Empezamos con el número diez."),

 dict(src=["BS@20-430", "CC@60-380"], label="¿QUIÉN LO CREÓ?", cap="#10",
      txt="Número diez: nadie se pone de acuerdo sobre quién lo inventó. Dos hombres dijeron ser el padre de Gasparín: Seymour Reit y Joe Oriolo, que trabajaban como animadores en los estudios Fleischer. Según Oriolo, la idea nació una noche de Halloween, cuando su hija Joan, de cuatro años, le tenía miedo a la oscuridad. Él recortó un fantasma amigable de cartón y lo colgó en un árbol del patio, para enseñarle que no todos los fantasmas son malos. Su hija confirmó esa historia."),
 dict(src=["BP@20-300", "BS@120-430"], label="¿QUIÉN LO CREÓ?", cap="REIT CONTRA ORIOLO",
      txt="Pero Seymour Reit contaba otra cosa. Decía que Gasparín nació de un cuento que él pensó y escribió solo, y que se lo dio a Oriolo para que lo ilustrara. Reit lo resumió así: Joe dibujó al personaje, pero el concepto, la idea y la historia eran suyos, y él era el verdadero papá de Gasparín. Los dos sostuvieron su versión durante décadas, y la discusión nunca se resolvió del todo."),

 dict(src=["CC@100-380", "BM@100-390"], label="LA VENTA", cap="#9",
      txt="Número nueve: lo vendieron por ciento setenta y cinco dólares. Reit y Oriolo querían vender la historia a los estudios Fleischer o a una editorial de libros infantiles, y llegaron a tener un acuerdo con la editorial Grosset and Dunlap. Pero Reit se fue a servir en la Segunda Guerra Mundial antes de que saliera el libro. Y mientras él estaba lejos, Oriolo vendió los derechos a Famous Studios, el estudio de Paramount que había reemplazado a Fleischer."),
 dict(src=["BS@200-430", "CC@200-380"], label="LA VENTA", cap="UN SOLO PAGO",
      txt="El precio total fue de ciento setenta y cinco dólares, en un solo pago. Fue todo lo que Oriolo recibió en su vida por el personaje: nada de las películas, ni de los cómics, ni de los juguetes que vendrían después. Y Reit, por su parte, no recibió ni un centavo por el libro. Y el fantasmita terminaría generando millones para otros."),

 dict(src=["FG@30-540", "FG@90-540"], label="EL PRIMER CORTO", cap="#8",
      txt="Número ocho: el primer corto es mucho más oscuro de lo que recuerdas. Se llamó The Friendly Ghost, El fantasma amigable, y lo dirigió Isadore Sparber en 1945. Empieza en una casa abandonada, donde Gasparín está leyendo un libro de verdad: Cómo ganar amigos, de Dale Carnegie. Cada noche, a la medianoche, los demás fantasmas salen a asustar a la gente. Pero Gasparín prefiere quedarse, porque lo que él quiere es hacer amigos con los vivos. Así que una noche se despide de su gato y se va de casa."),
 dict(src=["FG@150-540", "FG@210-540"], label="EL PRIMER CORTO", cap="LAS VÍAS DEL TREN",
      txt="Al día siguiente, todos los animales que saluda salen huyendo: un gallo, un topo que se pone los lentes y descubre que es un fantasma, un ratón, un gato y unas gallinas que se van volando con todo y gallinero. Y aquí viene lo inesperado. Junto a unas vías, triste porque nadie quiere ser su amigo, Gasparín se acuesta frente al tren que se acerca, con la idea de acabar con todo. Se le olvida que ya es un fantasma. El tren le pasa por encima sin tocarlo, y él se pone a llorar."),
 dict(src=["FG@300-540", "FG@420-540"], label="EL PRIMER CORTO", cap="BONNIE Y JOHNNY",
      txt="Entonces aparecen dos niños, Bonnie y Johnny, que sí quieren jugar con él. Su mamá se asusta al verlo, pero justo llega un banquero codicioso a cobrar la hipoteca de la casa. El banquero ve al fantasma, rompe el papel y sale corriendo tan rápido que incendia un puente. La mamá, agradecida, acepta a Gasparín, y al final lo manda a la escuela con los niños, vestido como un niño más. El narrador era Frank Gallop, y la voz de Gasparín la hizo Cecil Roy."),

 dict(src=["GB@60-510", "HW@40-480"], label="EL REDISEÑO", cap="#7",
      txt="Número siete: Gasparín no tuvo su propia serie de inmediato. Después del primer corto, solo apareció en dos más: There's Good Boos To-Night, de 1948, y A Haunting We Will Go, de 1949. Los tres salieron como parte de la serie Noveltoons de Paramount, y no fue sino hasta 1950 que empezó oficialmente la serie de Gasparín. En esos cortos ya se veía distinto: más redondito, más tierno y más infantil que en su debut. El animador Myron Waldman dijo que ese rediseño había sido idea suya."),
 dict(src=["HW@120-480", "HW@260-480"], label="EL REDISEÑO", cap="SIN RENOVAR",
      txt="Y hay otro detalle curioso. El primer corto, The Friendly Ghost, tenía su aviso de derechos de autor, pero nadie lo renovó cuando tocaba, como exigía la ley de Estados Unidos en esa época. Así que hoy es de dominio público, y cualquiera puede verlo gratis en el Archivo de Internet. Gracias a eso puedes ver aquí estas imágenes de la primera aparición de Gasparín."),

 dict(src=["GB@60-510", "GB@180-510"], label="FERDIE", cap="#6",
      txt="Número seis: en su segundo corto, Gasparín pierde a su único amigo. En There's Good Boos To-Night, de 1948, Gasparín por fin conoce a alguien que no huye de él: un zorrito llamado Ferdie. Juegan juntos, se esconden, se hacen amigos de verdad. Y entonces, el tono del corto cambia por completo. Llega un cazador con sus perros, y empiezan a perseguir al zorrito por el bosque."),
 dict(src=["GB@300-510", "GB@420-510"], label="FERDIE", cap="UN FINAL INESPERADO",
      txt="Gasparín logra asustar al cazador y a los perros, pero cuando termina la persecución, descubre que Ferdie está muerto. Es una escena muy fuerte para una caricatura de niños. El final, eso sí, tiene un giro: Ferdie regresa como fantasma, para quedarse para siempre con su amigo Gasparín en el más allá. Para muchos historiadores, este es el corto más oscuro de toda la serie."),

 dict(src=["BS@20-430", "BM@60-390"], label="SIEMPRE IGUAL", cap="#5",
      txt="Número cinco: los críticos decían que todos los cortos eran iguales. La serie de cine de Gasparín duró de 1950 a 1959, y casi todos los episodios seguían la misma fórmula. Gasparín se escapa del mundo de los fantasmas porque está cansado de asustar, intenta hacer amigos, todos huyen de él, y al final encuentra a un pequeño amigo, lo salva de algún peligro, y por fin lo aceptan. En total, el personaje apareció en cincuenta y cinco cortos de cine entre 1945 y 1959."),
 dict(src=["CC@100-380", "BP@100-300"], label="SIEMPRE IGUAL", cap="LEONARD MALTIN",
      txt="El historiador de animación Leonard Maltin, en su libro Of Mice and Magic, lo dijo sin piedad: Gasparín era el personaje más monótono que había invadido el mundo de las caricaturas desde el Súper Ratón, porque cada episodio parecía seguir la misma historia con pequeñas variaciones. Y hasta uno de los animadores, Lee Mishkin, se quejaba de que nunca sabías en qué película estabas trabajando, porque todas eran exactamente iguales."),

 dict(src=["BM@60-390", "BM@200-390"], label="LOS CÓMICS", cap="#4",
      txt="Número cuatro: los cómics salvaron a Gasparín. Su primera historieta salió en agosto de 1949, con la editorial St. John, que publicó solo cinco números. En 1952, Alfred Harvey, el dueño de Harvey Comics, empezó a publicar sus propios cómics de Gasparín. Los escribía y editaba Sid Jacobson, y los dibujaba Warren Kremer. Y ellos rompieron con la fórmula de los cortos."),
 dict(src=["BS@150-430", "BP@200-300"], label="LOS CÓMICS", cap="LE DIERON PIES",
      txt="Kremer le dibujó pies a Gasparín, evitaron insistir en que era un niño fallecido, le dieron un grupo de amigos, y empezaron a escribir historias donde usaba sus poderes para hacer el bien. De esos cómics nacieron otros personajes muy populares: Spooky, el fantasmita rudo; Wendy, la brujita buena; y el Trío Fantasmal, los tres tíos malvados de Gasparín. En 1959, Harvey compró el personaje de forma definitiva, junto con otras estrellas de Famous Studios."),

 dict(src=["BP@20-300", "BP@150-300"], label="BARBIE", cap="#3",
      txt="Número tres: Gasparín ayudó a presentar a la muñeca Barbie. Después de que Harvey compró los derechos en 1959, los cortos de Gasparín llegaron a la televisión en un programa de la cadena ABC llamado Matty's Funday Funnies. El patrocinador era la juguetería Mattel. Y en ese programa, Mattel presentó al público a una muñeca nueva que acababa de lanzar: Barbie. Mientras los niños veían al fantasma amigable, conocían también a la muñeca más famosa del mundo."),
 dict(src=["CC@200-380", "BS@300-430"], label="BARBIE", cap="EL MUÑECO QUE HABLA",
      txt="La relación con Mattel siguió. En 1961, la compañía lanzó un muñeco de Gasparín que hablaba, y la voz se la puso June Foray, una de las actrices de voz más famosas de la animación. Después vinieron más series de televisión: El nuevo show de Gasparín, en los sesenta; Gasparín y los ángeles, en 1979; y muchas más, hasta llegar a los años dos mil."),

 dict(src=["BM@100-390", "BM@250-390"], label="DE LA LUNA A ROGER RABBIT", cap="#2",
      txt="Número dos: Gasparín viajó a la Luna. En 1972, la misión Apolo 16 de la NASA llevó dos naves. Y el módulo de mando, la nave que se quedó en órbita alrededor de la Luna, tenía como nombre de llamada Casper, el nombre original de Gasparín en inglés. Su piloto, Ken Mattingly, explicó que ya había suficientes cosas serias en ese vuelo, así que eligió un nombre que no fuera serio."),
 dict(src=["CC@250-380", "HW@300-480"], label="DE LA LUNA A ROGER RABBIT", cap="LA ESCENA CORTADA",
      txt="Y casi aparece en ¿Quién engañó a Roger Rabbit?, la película de 1988. Gasparín era uno de los personajes que se consideraron para el funeral de Marvin Acme: iba a salir de la tumba mientras bajaban el ataúd, y asustar a todos los que estaban de luto. La escena se dibujó en el guion gráfico, pero se cortó antes de animarse. Así que el fantasma más famoso de las caricaturas se quedó fuera de una de las películas de caricaturas más famosas."),
 dict(src=["BS@250-430", "BP@250-300"], label="DE LA LUNA A ROGER RABBIT", cap="EL TRÍO Y LOS CAZAFANTASMAS",
      txt="Y hay otra historia de tribunales. En los años ochenta, Harvey se enfrentó en una demanda con Columbia Pictures, el estudio de Los cazafantasmas. Y el resultado sorprendió: el tribunal determinó que los derechos de Fatso, uno de los tíos del Trío Fantasmal, habían caducado, y que el personaje había pasado al dominio público. Años después, un investigador encontró que Harvey tampoco había renovado los derechos de otros de sus fantasmas, incluido el propio Gasparín."),

 dict(src=["CC@30-380", "BM@300-390"], label="LA PELÍCULA DE 1995", cap="#1",
      txt="Y el número uno: en 1995, Gasparín hizo historia en el cine. Universal estrenó Casper, una película con actores reales, donde Gasparín y sus tíos del Trío Fantasmal estaban hechos completamente por computadora. Fue el primer personaje creado por computadora en protagonizar una película. Y por primera vez en toda la historia del personaje, alguien se atrevió a contar cómo había muerto."),
 dict(src=["BS@330-430", "CC@300-380"], label="LA PELÍCULA DE 1995", cap="CASPER McFADDEN",
      txt="En la película, Gasparín era Casper McFadden, un niño de doce años que vivía en la mansión Whipstaff con su papá, un inventor. Un día jugó afuera en el frío hasta que se hizo de noche, y murió de neumonía. Es la única vez que la serie habla directamente de su muerte. En una escena, Gasparín vuelve a estar vivo por un momento, y ahí lo interpreta Devon Sawa, el único actor que ha hecho al personaje en carne y hueso."),
 dict(src=["FG@480-540", "GB@450-510"], label="LA PELÍCULA DE 1995", cap="DE LA TUMBA AL CINE",
      txt="Y eso cierra el círculo. Porque ya en los cortos originales de Famous Studios, Gasparín aparecía junto a una tumba con su nombre, una pista de que era un fantasma de verdad. Hicieron falta cincuenta años para que una película se animara a contar esa historia. El fantasmita que se vendió por ciento setenta y cinco dólares terminó siendo una estrella del cine moderno."),

 dict(src=["BP@250-300", "HW@400-480"], label=L, cap="",
      txt="Esos fueron diez datos increíbles sobre Gasparín, el fantasma amigable. ¿Cuál de estos no sabías? ¿Sabías que había ayudado a presentar a Barbie, o que viajó en el Apolo dieciséis? Cuéntanos en los comentarios. Y suscríbete, porque en este canal seguimos desenterrando los secretos de las caricaturas clásicas."),
]
json.dump(S, open("script.json", "w"), ensure_ascii=False, indent=1)
print(len(S), sum(len(s["txt"].split()) for s in S))
