import json
L = "VILLANOS QUE GANARON"
A = "EL JINETE SIN CABEZA · 1934"
B = "LA INICIACIÓN DE BIMBO · 1931"
T = "LA TORTUGA GANA · 1943"
G = "EL GREMLIN · 1943"
P = "EL HOTEL · 1943"
D = "EL HOMBRECITO · 1945"
S = [
 dict(src=["BI@60-330", "DD@380-410"], label=L, cap="",
      txt="En las caricaturas clásicas hay una regla que casi nunca se rompe: el malo pierde. El coyote se cae del barranco, Silvestre se queda sin el pajarito, y el cazador termina con la cara llena de hollín. Pero de vez en cuando, en algún estudio, alguien decidió romper la regla. Y el villano se salió con la suya."),
 dict(src=["FH@420-495", "PF@430-505"], label=L, cap="SEIS FINALES SIN JUSTICIA",
      txt="Hoy te cuento seis caricaturas clásicas, de los años treinta y cuarenta, donde el villano gana de verdad. No es que casi gane, ni que gane un ratito antes del último chiste. Gana al final, cuando aparece el letrero de fin. Revisamos el final de cada una, y en todas, el que se queda con el premio es el malo. Y ojo, porque el número uno no se escapa ni en el más allá. Empezamos con el número seis."),

 dict(src=["HH@25-120", "HH@85-200"], label=A, cap="#6",
      txt="En 1934, Ub Iwerks, el animador que había ayudado a Walt Disney a crear a Mickey Mouse, ya tenía su propio estudio, con una serie a todo color llamada ComiColor. Una de esas caricaturas fue El jinete sin cabeza, basada en La leyenda de Sleepy Hollow, el cuento que Washington Irving publicó en 1820. Y fue la primera vez que Iwerks usó la animación multiplano, que separaba los fondos en capas para dar sensación de profundidad."),
 dict(src=["HH@120-240", "HH@170-300"], label=A, cap="DOS PRETENDIENTES",
      txt="La historia es la de siempre. Dos hombres quieren a Katrina Van Tassel: el flaco maestro Ichabod Crane y el grandote y presumido Brom Bones. En la fiesta de la granja, los dos le dan de comer y le besan el brazo, y en la confusión terminan besándose entre ellos. Luego llega el baile. Brom tropieza con sus propios pies, e Ichabod baila mucho mejor."),
 dict(src=["HH@250-340", "HH@300-390"], label=A, cap="UNA SERPIENTE Y UN ZORRILLO",
      txt="Ichabod se luce con un zapateado, y Katrina queda impresionada. Brom está furioso, tan furioso que se imagina a Ichabod como una serpiente de cascabel, como un zorrillo apestoso y como un burro. Entonces, junto a la chimenea, un anciano cuenta la leyenda del jinete sin cabeza. Todos se asustan. Y a Brom se le ocurre una idea."),
 dict(src=["HH@410-475", "HH@440-482"], label=A, cap="EL DISFRAZ",
      txt="Esa noche, Katrina saca a Ichabod de la casa a patadas. Y en el camino de regreso, un jinete sin cabeza lo persigue por el bosque hasta hacerlo huir aterrado. Pero no era ningún fantasma. Era Brom, disfrazado. El truco sucio funcionó a la perfección, y nadie lo descubre."),
 dict(src=["HH@298-500", "HH@470-500"], label=A, cap="LA BODA",
      txt="Y así termina: con la boda de Brom y Katrina. El tramposo se queda con la novia, y nadie lo castiga. Eso sí, Iwerks le regaló a Ichabod una pequeña venganza. En plena boda, ya con el anillo puesto, aparece una figura sin cabeza que espanta a todos, a los novios incluidos. Es Ichabod. Pero la boda ya estaba hecha. Brom ganó. Y no es un invento de Iwerks: en el cuento original de Irving, también es Brom el que termina casado con Katrina."),

 dict(src=["BI@15-120", "BI@60-200"], label=B, cap="#5",
      txt="Número cinco. En 1931, el estudio de Max Fleischer, en Nueva York, estrenó La iniciación de Bimbo. Bimbo era un perrito, la estrella de la serie Talkartoons. Aquí aparece una versión temprana de Betty Boop, que todavía tenía orejas y nariz de perrita. Y fue la última caricatura de Betty animada por Grim Natwick, uno de sus creadores, antes de irse a otro estudio."),
 dict(src=["BI@40-150", "BI@100-220"], label=B, cap="¿QUIERES SER MIEMBRO?",
      txt="Bimbo va caminando por la calle, silbando, y de pronto cae por una alcantarilla abierta. Alguien la cierra con llave detrás de él. Bimbo resbala por un tobogán hasta el sótano de una sociedad secreta, llena de encapuchados. El jefe le hace una sola pregunta: ¿quieres ser miembro? Y Bimbo dice que no."),
 dict(src=["BI@150-300", "BI@200-320"], label=B, cap="PRUEBAS DE PESADILLA",
      txt="Entonces empiezan las pruebas. Pisos que se abren, cuchillos, una puerta con el número trece, paredes que se cierran y sombras gigantes. Después de cada prueba, la misma pregunta. Y la misma respuesta: no. El crítico Leonard Maltin la llamó la más oscura de todas las caricaturas de los Fleischer."),
 dict(src=["BI@330-378", "BI@224-378"], label=B, cap="LA SOCIEDAD GANA",
      txt="Al final, el jefe se quita el disfraz, y resulta ser Betty Boop. Ella baila para Bimbo, y él por fin acepta. Todos los demás miembros se quitan la capucha, y todos son copias de Betty. La sociedad secreta consigue exactamente lo que quería desde el principio. Y en 1994, gente de la industria de la animación la votó en el lugar treinta y siete de las cincuenta mejores caricaturas de la historia."),

 dict(src=["TW@15-120", "TW@60-160"], label=T, cap="#4",
      txt="Número cuatro. En 1941, Tex Avery había hecho Tortoise Beats Hare, donde la tortuga Cecil le gana una carrera a Bugs Bunny con trampa. Y en 1943, Bob Clampett hizo la revancha: Tortoise Wins by a Hare. Dato curioso: fue la primera caricatura con el diseño de Bugs hecho por Robert McKimson."),
 dict(src=["TW@100-200", "TW@150-240"], label=T, cap="EL CHASIS AERODINÁMICO",
      txt="Bugs quiere saber el secreto de Cecil, así que se disfraza de anciano y va a preguntarle. La tortuga lo reconoce al instante, pero le sigue el juego. Le dice que su secreto es un chasis aerodinámico, le enseña los planos, y le explica que el diseño del conejo está todo mal, porque esas orejas largas frenan con el aire. Y de paso, le dice que los conejos son tontos."),
 dict(src=["TW@200-320", "TW@240-360"], label=T, cap="LA MAFIA DE LOS CONEJOS",
      txt="Bugs se fabrica su propio caparazón y se tapa las orejas con un gorro de hule. Mientras tanto, una banda de conejos gánsteres apuesta todo su dinero a que gana el conejo. Pero en la carrera, Bugs va disfrazado de tortuga. Y Cecil, muy listo, se disfraza de conejo. Así que los gánsteres atacan a Bugs creyendo que es la tortuga."),
 dict(src=["TW@380-450", "TW@420-455"], label=T, cap="CECIL GANA",
      txt="Bugs está a punto de ganar, pero los gánsteres lo detienen justo antes de la meta, y Cecil cruza primero. Bugs se quita el disfraz y les dice quién es en realidad, y los gánsteres entienden, demasiado tarde, que acaban de hacer ganar a la tortuga. El historiador Jerry Beck escribió que Clampett se burló a la vez de la fábula de Esopo, de la versión de Disney de 1935 y de la de Tex Avery."),

 dict(src=["FH@15-110", "FH@40-140"], label=G, cap="#3",
      txt="Número tres. En 1943, en plena Segunda Guerra Mundial, Bob Clampett dirigió Falling Hare. Bugs está en una base aérea del ejército de Estados Unidos, leyendo un libro llamado La victoria por el poder de las liebres, una burla de la película de Disney La victoria por el poder aéreo. Y se ríe de lo que dice el libro sobre los gremlins, unas criaturitas que sabotean aviones."),
 dict(src=["FH@60-160", "FH@120-220"], label=G, cap="LA BOMBA",
      txt="Error. Un gremlin aparece y empieza a martillar la punta de una bomba gigante, justo donde Bugs está recostado. Bugs, muy amable, le ofrece ayuda, y está a punto de dar el golpe él mismo antes de darse cuenta. Por una vez, alguien le hace a Bugs lo que Bugs siempre les hace a los demás."),
 dict(src=["FH@220-380", "FH@300-420"], label=G, cap="EN PICADA",
      txt="El gremlin lo encierra en un avión y lo pone a despegar. Bugs pasa casi toda la caricatura perdiendo: esquiva rascacielos, se asusta tanto que cambia de color, y el avión cae en picada hacia la tierra a una velocidad que ni el indicador puede creer. El letrero del tablero dice: increíble, ¿no?"),
 dict(src=["FH@430-495", "FH@460-495"], label=G, cap="SIN GASOLINA",
      txt="Justo antes de estrellarse, el avión se detiene en el aire. Se acabó la gasolina. Y Bugs y el gremlin le explican al público que así son las cosas con el racionamiento de gasolina de la guerra. Dato curioso: Disney preparaba una película de gremlins basada en un libro de Roald Dahl, y pidió a otros estudios no usarlos. Por eso esta caricatura, que se iba a llamar Bugs Bunny y el gremlin, cambió de título. Uno de sus animadores fue Bill Meléndez, el que años después dirigiría las caricaturas de Charlie Brown y Snoopy. Y en 1972 entró al dominio público, porque nadie renovó su registro de derechos de autor."),

 dict(src=["PF@15-120", "PF@60-180"], label=P, cap="#2",
      txt="Número dos. En julio de 1943, Frank Tashlin dirigió Porky Pig's Feat, en blanco y negro. Porky y el Pato Lucas están hospedados en el hotel Broken Arms, algo así como el hotel Brazos Rotos. El problema es que no pueden pagar la cuenta, porque Lucas perdió todo el dinero jugando a los dados. Y un detalle para los oídos: fue la primera caricatura en usar Powerhouse, la pieza de Raymond Scott que después sonaría en muchísimas escenas de fábricas y máquinas de Warner."),
 dict(src=["PF@120-260", "PF@180-320"], label=P, cap="LA CUENTA",
      txt="Y la cuenta es una locura. El gerente les cobra cada lujo: el aire que respiran, la luz del sol, y hasta la buena voluntad. Así que deciden escapar sin pagar. Por el elevador, por la escalera de caracol, con sábanas amarradas desde la ventana, y saltando al edificio de enfrente. Y el gerente, un tipo enorme y muy tranquilo, les gana cada vez."),
 dict(src=["PF@380-470", "PF@430-480"], label=P, cap="ENCADENADOS",
      txt="Al final, el gerente los encierra en el cuarto con grilletes, hasta que paguen. Llega el invierno. Porky cuenta los días en la pared como un preso, y Lucas empieza a perder la cabeza. Desesperados, llaman a la única persona capaz de salir de cualquier trampa: Bugs Bunny."),
 dict(src=["PF@470-505", "PF@300-505"], label=P, cap="¿NO FUNCIONAN, VERDAD?",
      txt="Bugs les pregunta si ya probaron esto, y esto, y esto otro. Sí, ya lo probaron todo. Entonces se abre la puerta del cuarto de al lado, y ahí está Bugs, también encadenado. ¿No funcionan, verdad?, les dice. Fue la última de las tres apariciones de Bugs en blanco y negro, y la última de Porky en blanco y negro también. El gerente les ganó a los tres."),

 dict(src=["DD@15-90", "DD@40-120"], label=D, cap="#1",
      txt="Y el número uno. Enero de 1945. Bob Clampett estrena Draftee Daffy. El Pato Lucas lee en el periódico que las tropas de Estados Unidos están haciendo retroceder a los nazis, y se pone feliz, muy patriota. Hasta que suena el teléfono. Es la junta de reclutamiento. El ejército lo quiere a él."),
 dict(src=["DD@100-220", "DD@160-280"], label=D, cap="EL HOMBRECITO",
      txt="Y así aparece el villano más pequeño de esta lista: el hombrecito de la junta de reclutamiento, un señor bajito, calvo y de lentes redondos, que solo quiere entregarle un sobre. Lucas hace de todo para no recibirlo. Le cierra la puerta, se esconde, levanta barricadas, y hasta recurre a una bomba."),
 dict(src=["DD@280-370", "DD@360-385"], label=D, cap="EN CASO DE RECLUTAMIENTO",
      txt="Nada funciona. El hombrecito siempre aparece, sonriente, con su sobre. Desesperado, Lucas se sube a un cohete que tiene un letrero: úsese solo en caso de reclutamiento. El cohete despega, da la vuelta en el cielo y baja de nuevo a toda velocidad. Se estrella. Y Lucas termina en el infierno."),
 dict(src=["DD@385-410", "DD@244-410"], label=D, cap="NI EN EL INFIERNO",
      txt="Ahí, entre el fuego, Lucas por fin respira aliviado. Hasta que aparece un diablo, y debajo está el hombrecito de la junta, con su sobre. Lucas no pudo escapar ni en el infierno. El historiador Jerry Beck dijo que Clampett convirtió aquí al pato en un cobarde total, algo que Chuck Jones explotaría años después. Y la voz del hombrecito la hizo Mel Blanc, imitando a un personaje de radio muy famoso, The Great Gildersleeve."),
 dict(src=["HH@298-500", "TW@420-455"], label=L, cap="",
      txt="Seis caricaturas, seis villanos que se salieron con la suya: un tramposo con disfraz, una sociedad secreta, una tortuga muy lista, un gremlin, un gerente de hotel y un burócrata con un sobre. ¿Cuál te parece el final más injusto? Cuéntanos en los comentarios, y suscríbete para más secretos de la animación clásica."),
]
json.dump(S, open("script.json", "w"), ensure_ascii=False, indent=1)
print(len(S), sum(len(s["txt"].split()) for s in S))
