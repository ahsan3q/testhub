import json
L = "COLONEL BLEEP · 1957"
S = [
 dict(src=["AE@30-249", "KW@30-315"], label=L, cap="",
      txt="Un extraterrestre con cabeza triangular, un hombre de las cavernas despertado por una bomba atómica y un muñeco vaquero que no podía hablar. Así eran los héroes de Colonel Bleep, una caricatura de 1957 que casi nadie recuerda. Pero esta serie rara, hecha en Miami con muy poco dinero, tiene un récord que ni Disney ni Hanna-Barbera le pueden quitar."),
 dict(src=["LL@30-320", "TP@30-324"], label=L, cap="10 DATOS INCREÍBLES",
      txt="Hoy te cuento diez datos increíbles sobre Colonel Bleep: cómo nació, por qué más de la mitad de sus episodios desaparecieron, cómo terminó siendo de todos, y cómo llegó a inspirar a los creadores de Ren y Stimpy y hasta a una serie de televisión moderna. Algunos de estos datos parecen de ciencia ficción, igual que la caricatura. Empezamos con el número diez."),

 dict(src=["AE@60-249", "DB@40-290"], label="LA PRIMERA EN COLOR", cap="#10",
      txt="Número diez: fue la primera serie de caricaturas en color hecha para la televisión. Antes de Colonel Bleep, la mayoría de las caricaturas que se veían en televisión eran cortos viejos de cine, o producciones en blanco y negro. Colonel Bleep se pensó desde el principio para la pantalla de la casa, y se filmó en color. Por eso aparece en los libros de historia de la animación, aunque casi nadie la haya visto."),
 dict(src=["MM@30-225", "KD@40-345"], label="LA PRIMERA EN COLOR", cap="1956 · 1957",
      txt="La serie la crearon y escribieron Robert D. Buchanan y Jack Schleh, y su registro de creación tiene fecha del ocho de junio de 1956. Se estrenó en sindicación el veintiuno de septiembre de 1957, como un segmento dentro de un programa infantil llamado Uncle Bill's TV Club. Es decir, no tenía su propio horario: llegaba metida dentro de otro programa, como una sorpresa para los niños."),

 dict(src=["TF@40-330", "PP@30-318"], label="DE BUFFALO A MIAMI", cap="#9",
      txt="Número nueve: el estudio nació en la nieve y terminó en la playa. La compañía que la animó se llamaba Soundac. Se fundó en 1951 en Buffalo, Nueva York, por un hombre llamado Bobby Nicholson. Cuando Nicholson se fue, Robert Buchanan tomó su lugar. Y en 1955, el estudio se mudó completo a Miami, en Florida. Desde ahí, con el calor del sur, salió la primera serie animada en color de la televisión."),
 dict(src=["KW@60-315", "LL@60-320"], label="DE BUFFALO A MIAMI", cap="UN PROGRAMA COMPLETO",
      txt="Y la idea original era más grande. Se conserva una colección de segmentos para un programa con presentador, donde las caricaturas de Colonel Bleep serían la base de un show infantil completo, con concursos, adivinanzas y actividades para los niños. Ese material lo patrocinaba Loblaws, una cadena de supermercados canadiense que tenía tiendas en la zona de Buffalo. Es posible que se haya transmitido por WGR, el canal dos de esa ciudad."),

 dict(src=["TP@60-324", "AE@100-249"], label="UNA SOLA VOZ", cap="#8",
      txt="Número ocho: toda la serie tenía prácticamente una sola voz. El narrador era Noah Tyler, un presentador de noticias local de Miami. Él contaba cada historia y hacía casi todas las voces de los personajes. Y aquí está el truco: la mayoría de los personajes no hablaban. Colonel Bleep se comunicaba con pitidos, y los demás se expresaban con gestos y efectos de sonido. Así se ahorraban todo un elenco de actores."),
 dict(src=["DB@80-290", "MM@60-225"], label="UNA SOLA VOZ", cap="ANIMACIÓN LIMITADA",
      txt="El director de todos los episodios fue el propio Jack Schleh. Y la animación era extremadamente limitada, como casi toda la animación de televisión de esa época. Muchas veces los personajes se quedan casi quietos, mientras la voz del narrador empuja la historia. Pero esa limitación se convirtió en estilo: fondos de colores intensos, figuras blancas y líneas simples que se ven muy distintas a cualquier caricatura de cine de esos años."),

 dict(src=["AE@130-249", "PP@60-318"], label="UNA BOMBA ATÓMICA", cap="#7",
      txt="Número siete: toda la historia empieza con una bomba atómica. Según la premisa de la serie, en 1945, la primera explosión nuclear en la Tierra tuvo efectos cósmicos. Un cavernícola de la Edad de Piedra, que estaba hibernando, despertó con la explosión y fue transportado al presente. Se llama Scratch. Y muy lejos de aquí, en un planeta llamado Futura, sus habitantes se alarmaron al detectar la explosión."),
 dict(src=["AE@160-249", "KD@80-345"], label="UNA BOMBA ATÓMICA", cap="PASADO, PRESENTE Y FUTURO",
      txt="Así que los futurianos, unos extraterrestres con cabeza triangular y cuerpo delgado, mandaron a uno de los suyos a investigar: el Coronel Bleep. Al llegar a la Tierra, Bleep nombra a Scratch su ayudante. Bleep representa el futuro y Scratch representa el pasado. Y el presente lo representa Squeak, un muñeco con sombrero de vaquero, descrito como un niño alegre, muy parecido a ti, que estás viendo la caricatura."),

 dict(src=["TF@80-330", "KW@100-315"], label="EL MUÑECO MUDO", cap="#6",
      txt="Número seis: Squeak era un títere que se movía solo, pero no podía hablar. La explicación era sencilla: como es un muñeco, no tiene voz propia. Era un exactor que se movía por voluntad propia, sin que nadie explicara cómo. Pero esa idea no duró para siempre. Con el tiempo se abandonó, y en algunos de los episodios posteriores Squeak termina diciendo algunas palabras. Ni la caricatura respetó del todo sus propias reglas."),
 dict(src=["LL@100-320", "TP@100-324"], label="EL MUÑECO MUDO", cap="LA ISLA CERO CERO",
      txt="Juntos, los tres instalaron su base en la Isla Cero Cero, en el océano Atlántico, para proteger al sistema solar de amenazas extraterrestres. Bleep llevaba un casco transparente como burbuja, con una hélice y dos antenas. La hélice, junto con su inseparable monociclo, lo ayudaba a viajar por el espacio. Y Scratch tenía una fuerza sobrehumana y un garrote enorme. Squeak, en cambio, no tenía ningún superpoder conocido."),

 dict(src=["KD@120-345", "MM@100-225"], label="ENERGÍA FUTÓMICA", cap="#5",
      txt="Número cinco: Bleep usaba una energía inventada para la serie, la energía futómica, una mezcla de las palabras futuro y atómico. Salía de sus antenas, normalmente como un rayo. Pero tenía límites. La cantidad de energía que Bleep podía acumular era finita, y en algunos episodios se queda sin carga y queda vulnerable. En otros, el calor del rayo es peligroso, y tiene que buscar otra salida. Hasta su hélice podía usarse como taladro."),
 dict(src=["PP@100-318", "DB@120-290"], label="ENERGÍA FUTÓMICA", cap="LOS VILLANOS",
      txt="Y como todo héroe, tenía villanos que regresaban. El principal era el Doctor Destructo, un villano encapuchado que escapó de los anillos de Saturno al principio de la serie. También estaban Bruto, el Robot Negro, que había sido su secuaz; Black Patch, un pirata espacial; y el Caballero Negro de Plutón. Los viajes entre planetas los hacían robots, y una estación espacial llamada X-1 servía como central de transporte."),

 dict(src=["KW@130-315", "LL@130-320"], label="EPISODIOS PERDIDOS", cap="#4",
      txt="Número cuatro: más de la mitad de la serie está perdida. Se produjeron cien episodios, de entre tres y seis minutos cada uno. Pero hoy solo se conocen cuarenta y cinco que existen en alguna forma, y ocho de ellos solo sobreviven en blanco y negro. Y a diferencia de otras caricaturas de televisión de la época, que en su mayoría se conservaron, casi no queda ningún material original de la producción de Colonel Bleep."),
 dict(src=["TF@120-330", "AE@190-249"], label="EPISODIOS PERDIDOS", cap="¿QUÉ PASÓ?",
      txt="¿Dónde quedaron los negativos, los dibujos y los guiones? Nadie lo sabe con certeza. Existen historias sobre cómo se perdió el material, pero ninguna está confirmada, así que no te voy a contar una leyenda como si fuera un hecho. Lo único seguro es el resultado: la primera serie animada en color de la televisión es hoy, en buena parte, un rompecabezas incompleto."),

 dict(src=["TP@130-324", "PP@130-318"], label="DOMINIO PÚBLICO", cap="#3",
      txt="Número tres: terminó siendo de todos. La serie se siguió transmitiendo por muchos años, y hay registros de que salió al aire todavía en 1971. Pero los derechos de autor de los episodios vencieron en 1985 sin que nadie los renovara. Desde entonces, Colonel Bleep está en el dominio público. Eso significa que cualquiera puede verla, copiarla y compartirla, y por eso hoy la puedes encontrar completa en el Internet Archive."),
 dict(src=["DB@150-290", "KD@160-345"], label="DOMINIO PÚBLICO", cap="EL ERROR QUE LA SALVÓ",
      txt="Y lo curioso es que ese descuido ayudó a mantenerla viva. Como nadie era dueño de la serie, coleccionistas, archivistas y aficionados pudieron compartir los episodios que iban encontrando, sin pedirle permiso a nadie. Si los derechos se hubieran renovado, quizá estos episodios seguirían guardados en una bodega. Las imágenes que estás viendo ahora mismo existen en internet gracias a ese vencimiento."),

 dict(src=["LL@160-320", "MM@130-225"], label="BÚSQUEDA DEL TESORO", cap="#2",
      txt="Número dos: los episodios siguen apareciendo en los lugares más raros. En 1991, Streamline Pictures publicó dos videocasetes con casi todos los episodios conocidos en ese momento. Según se cuenta, salieron de la bodega de un canal de televisión del suroeste de Estados Unidos, que había transmitido la serie, durante un proceso de bancarrota. Y el veintitrés de agosto de 2005, Alpha Video lanzó un DVD con veintitrés episodios, unos veinte de ellos nunca vistos en video."),
 dict(src=["KW@160-315", "TF@160-330"], label="BÚSQUEDA DEL TESORO", cap="2018 · 2019",
      txt="En septiembre de 2018, el historiador de animación Jerry Beck encontró, en el archivo de Mark Kausler, los segmentos en blanco y negro del programa con presentador, incluida la secuencia de títulos original. Y el doce de septiembre de 2019, se subieron a YouTube ocho episodios que se creían perdidos, en copias de tono sepia. Un mes después, el diecinueve de octubre, apareció un noveno, llamado Winner Take All. Todos venían del archivo personal de Ron Kurer y su sitio Toon Tracker."),
 dict(src=["LL@190-320", "TP@160-324"], label="BÚSQUEDA DEL TESORO", cap="EL CARTERO MALICIOSO",
      txt="Y la búsqueda no ha terminado. En marzo de 2023, la archivista Sarah Smith descubrió un episodio perdido llamado The Malicious Mailman, el cartero malicioso. Es la continuación de un episodio que sí conocíamos, The Lunar Luger, que es justo el que estás viendo. Ese episodio rescatado se restauró en Multicom Entertainment Group y se estrenó el veintitrés de agosto de 2023 en el servicio de streaming The Archive."),

 dict(src=["AE@200-249", "KW@190-315"], label="SU HERENCIA", cap="#1",
      txt="Y el número uno: esta caricatura olvidada dejó huella en la animación moderna. Las notas de producción de The Ren and Stimpy Show mencionan a Colonel Bleep como una inspiración para sus animadores. Y en el episodio Space Madness, Locura espacial, de Ren y Stimpy, aparece una recreación de la secuencia de títulos de Colonel Bleep. Es un homenaje que casi nadie notó, porque casi nadie conocía la caricatura original."),
 dict(src=["KD@200-345", "PP@160-318"], label="SU HERENCIA", cap="DE SEVERANCE A LOS VIDEOJUEGOS",
      txt="Pero no es lo único. Un clip del episodio The Killer Whale, la orca asesina, aparece en la segunda temporada de la serie Severance, en el episodio The After Hours. Y en 2026, Colonel Bleep llegó a los videojuegos: aparece en Royalty Free-For-All, un juego de pelea dedicado a personajes de dominio público, que salió el once de agosto de 2026, con Squeak y Scratch como invocaciones y el Doctor Destructo como objeto."),

 dict(src=["TP@190-324", "DB@180-290"], label="EL ESTILO GOOGIE", cap="EL FUTURO DE LOS AÑOS 50",
      txt="Antes de despedirnos, fíjate en el diseño. Colonel Bleep está muy influido por el estilo googie, la estética futurista de los años cincuenta y principios de los sesenta en Estados Unidos. Naves espaciales angulares con enormes aletas, letreros con forma de bumerán y símbolos atómicos por todas partes, sobre todo para representar la energía futómica de Bleep. Es el futuro tal como lo imaginaba la gente en 1957."),
 dict(src=["MM@160-225", "LL@220-320"], label="EL ESTILO GOOGIE", cap="EL COLOR QUE POCOS VIERON",
      txt="Y hay una ironía final. Colonel Bleep fue la primera serie animada en color para la televisión, pero en 1957 los televisores a color eran escasos y caros. Así que la mayoría de los niños que la vieron en su estreno seguramente la vieron en blanco y negro. Los colores intensos que ves hoy, esos fondos azules y rojos, eran una apuesta por el futuro, igual que el propio Coronel Bleep."),
 dict(src=["TF@200-330", "KW@220-315"], label="LOS MISMOS CREADORES", cap="MIGHTY MISTER TITAN",
      txt="Los creadores no se detuvieron ahí. Jack Schleh y Robert Buchanan también produjeron, con Soundac, una serie de caricaturas de ejercicio físico para niños, llamada The Mighty Mister Titan. Se estrenó el primero de enero de 1964 y tuvo cien episodios. Pero ninguna de sus producciones alcanzó el lugar que tiene Colonel Bleep en la historia: la primera."),

 dict(src=["AE@220-249", "TP@220-324"], label=L, cap="",
      txt="Un estudio que se mudó de la nieve a la playa, un presentador de noticias que hacía todas las voces, una serie que perdió más de la mitad de sus episodios y que terminó siendo de todos por un trámite que nadie hizo. ¿Habías visto alguna vez a Colonel Bleep? ¿O lo conociste hoy? Cuéntanos en los comentarios, y suscríbete para más historias de las caricaturas clásicas."),
]
json.dump(S, open("script.json", "w"), ensure_ascii=False, indent=1)
print(len(S), sum(len(s["txt"].split()) for s in S))
