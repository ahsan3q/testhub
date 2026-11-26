import json
L = "CARICATURAS DE 1961"
M = "EL MUNDO EN 1961"
S = [
 dict(src=["NF@60-440", "AS@40-356"], label=L, cap="",
      txt="En 1961, una jirafa cantante dejó África para triunfar en Nueva York. Un vikingo llamado Sam trató de conquistar un castillo y terminó derrotado por un conejo y un elefante. Un yeti confundió a un pato con un conejo, y el coyote se lanzó cuesta abajo en esquís con rueditas. ¿Los recuerdas? Seguramente alguna de esas escenas te suena, aunque no sepas cómo se llamaba la caricatura."),
 dict(src=["PV@40-376", "LS@40-376"], label=L, cap="6 CARICATURAS OLVIDADAS",
      txt="Hoy seguimos nuestro viaje año por año, y llegamos a 1961. Te traigo seis caricaturas de esa temporada que casi nadie menciona. Todas salieron del estudio de Warner Brothers, el de Bugs Bunny, el Pato Lucas, Silvestre y el Correcaminos. Y la número uno estuvo nominada al Óscar. Pero antes, como siempre, un poco de contexto sobre cómo era el mundo en 1961."),

 dict(src=["IN@40-300", "IN@60-300"], label=M, cap="UN PRESIDENTE JOVEN",
      txt="El veinte de enero de 1961, John F. Kennedy tomó posesión como presidente de Estados Unidos, frente al Capitolio, en Washington, en un día helado. Tenía cuarenta y tres años, y era el presidente más joven elegido en la historia de su país. Las imágenes que estás viendo son de esa ceremonia, filmadas por un noticiero de la época."),
 dict(src=["IN@150-300", "IN@200-300"], label=M, cap="NO PREGUNTES",
      txt="En su discurso dijo una frase que se volvió famosa en todo el mundo: no preguntes qué puede hacer tu país por ti; pregunta qué puedes hacer tú por tu país. Después vino el desfile, y en la noche los bailes de gala. Fue el principio de una década llena de cambios, y también de una carrera que ese mismo año iba a acelerar como nunca: la carrera hacia el espacio."),
 dict(src=["GG@10-70", "GG@30-70"], label=M, cap="EL PRIMER HOMBRE EN EL ESPACIO",
      txt="El doce de abril de 1961, la Unión Soviética lanzó la nave Vostok uno, con el cosmonauta Yuri Gagarin a bordo. Fue el primer ser humano en llegar al espacio y en dar una vuelta completa alrededor de la Tierra. El vuelo duró ciento ocho minutos, desde el despegue hasta el aterrizaje. Días después, Moscú lo recibió como a un héroe, y eso es lo que estás viendo: retratos de Gagarin por todas partes."),
 dict(src=["GG@44-70", "GG@12-40"], label=M, cap="UNA VUELTA AL MUNDO",
      txt="Y hay detalles de ese vuelo que poca gente conoce. La nave de Gagarin llegó a una altura máxima de más de trescientos kilómetros sobre la Tierra. Y Gagarin no aterrizó dentro de su cápsula: a unos siete kilómetros de altura, salió expulsado de la nave y bajó en su propio paracaídas, separado de ella. Desde ese día, la carrera espacial entre las dos potencias se volvió también una competencia de imagen frente a todo el mundo."),
 dict(src=["SH@10-103", "SH@60-103"], label=M, cap="LA RESPUESTA DE ESTADOS UNIDOS",
      txt="Estados Unidos respondió menos de un mes después. El cinco de mayo de 1961, Alan Shepard voló en la cápsula Freedom 7. Fue un vuelo suborbital de unos quince minutos, sin dar la vuelta a la Tierra, pero llegó a más de ciento ochenta kilómetros de altura. Cayó en paracaídas en el océano Atlántico, y un helicóptero lo llevó a un portaaviones. Días después fue recibido en Washington con un desfile."),
 dict(src=["LS@60-376", "HD@60-370"], label=M, cap="DON GATO Y SU PANDILLA",
      txt="Y en la televisión también hubo noticias. El veintisiete de septiembre de 1961, la cadena ABC estrenó Top Cat, de Hanna y Barbera, que en América Latina conocimos como Don Gato y su pandilla. Se transmitía en horario estelar, pero en Estados Unidos fue un fracaso de audiencia y solo duró una temporada, de treinta episodios. Sin embargo, en nuestros países se volvió un clásico. Y ahora sí, empezamos con la cuenta regresiva."),

 dict(src=["HD@40-370", "HD@60-370"], label="HOPPY DAZE", cap="#6",
      txt="Número seis: Hoppy Daze, dirigida por Robert McKimson. La historia pasa en un muelle, entre bodegas y cajas de carga. Ahí vive Silvestre, el gato, y un gatito callejero con sombrero de bombín que lo admira y quiere aprender a cazar ratones. Silvestre acepta enseñarle, y se ve a sí mismo como el gran maestro. El problema es lo que hay dentro de una de esas cajas."),
 dict(src=["HD@120-370", "HD@140-370"], label="HOPPY DAZE", cap="BABY KANGAROO · AUSTRALIA",
      txt="La caja dice muy claro: bebé canguro, Australia, manejar con cuidado. Pero los gatos creen que lo que sale de ahí es un ratón gigante. Es Hippety Hopper, el canguro bebé que ya había vuelto loco a Silvestre en otras caricaturas. Y cada vez que Silvestre intenta atraparlo, el canguro lo manda volando de una patada, mientras el gatito observa y toma nota."),
 dict(src=["HD@220-370", "HD@300-370"], label="HOPPY DAZE", cap="EL MAESTRO",
      txt="Lo divertido de esta caricatura es la vergüenza de Silvestre. Él quiere quedar bien frente a su alumno, así que no puede admitir que le tiene miedo a un ratón que salta como un resorte. Cada golpe lo deja peor, pero él sigue fingiendo que todo es parte de la lección. Es una de esas caricaturas que se repitieron muchísimo en la televisión, aunque casi nadie recuerda su nombre."),

 dict(src=["MS@40-340", "MS@80-340"], label="THE MOUSE ON 57TH STREET", cap="#5",
      txt="Número cinco: The Mouse on 57th Street, el ratón de la calle cincuenta y siete, dirigida por Chuck Jones. El título hace referencia a una de las calles más elegantes de Nueva York, famosa por sus joyerías. Y la protagonista no es una estrella conocida, sino un ratoncito que vive entre vitrinas de lujo, pasteles finos y aparadores llenos de terciopelo."),
 dict(src=["MS@160-340", "MS@180-340"], label="THE MOUSE ON 57TH STREET", cap="EL DIAMANTE MÁS GRANDE",
      txt="En una de esas vitrinas está en exhibición el Sun-Flame, presentado como el diamante sin cortar más grande del mundo. Y de pronto, el diamante desaparece. Los periódicos lo anuncian en primera plana, la policía sale a buscar al ladrón por toda la ciudad, y dos agentes muy torpes terminan persiguiendo pistas que no llevan a ninguna parte. El culpable, claro, es mucho más pequeño de lo que todos imaginan."),
 dict(src=["MS@240-340", "MS@280-340"], label="THE MOUSE ON 57TH STREET", cap="UN PASTEL CON RON",
      txt="Y en medio de todo hay un pastel de ron, y un ratón que no está acostumbrado a tanto ron. No te voy a contar cómo termina, porque vale la pena verla. Lo que más llama la atención es el estilo: fondos muy modernos, colores planos y una Nueva York dibujada casi como un cartel de los años sesenta. Era el nuevo estilo de Chuck Jones y su diseñador, Maurice Noble."),

 dict(src=["PV@40-376", "PV@80-376"], label="PRINCE VIOLENT", cap="#4",
      txt="Número cuatro: Prince Violent, dirigida por Friz Freleng y su diseñador de toda la vida, Hawley Pratt. Se estrenó el dos de septiembre de 1961, con Bugs Bunny y Sam Bigotes. El título es un juego de palabras con Prince Valiant, el Príncipe Valiente, una tira cómica muy famosa en esa época. Y aquí Sam es un vikingo, Sam el Terrible, que llega remando por un río para invadir un castillo."),
 dict(src=["PV@100-376", "PV@140-376"], label="PRINCE VIOLENT", cap="EL ELEFANTE",
      txt="Sam entra al castillo sin problemas, pero ahí está Bugs, que lo desarma, se burla de su casco y lo saca a la fuerza. A partir de ahí, Sam intenta de todo para volver a entrar: catapultas con piedras, túneles por debajo de la muralla y hasta un elefante de guerra. Bugs lo frena con trucos cada vez más locos, como pintar una puerta falsa en la pared del castillo."),
 dict(src=["PV@300-376", "PV@340-376"], label="PRINCE VIOLENT", cap="EL TÍTULO PROHIBIDO",
      txt="Al final, el elefante termina ayudando sin querer a Bugs, y Sam se va derrotado, jurando venganza contra el conejo y el elefante. Bugs, por su parte, le regala cacahuates al elefante como premio. Y un dato curioso: durante décadas, esta caricatura se transmitió en televisión con otro título, Prince Varmint, que cambiaba la palabra violento por una que significa alimaña. Solo en los años 2020 volvió a verse con su título de estreno."),

 dict(src=["LS@40-376", "LS@60-376"], label="LICKETY-SPLAT", cap="#3",
      txt="Número tres: Lickety-Splat, del Coyote y el Correcaminos, dirigida por Chuck Jones y Abe Levitow. Se estrenó el tres de junio de 1961. El título es un juego con la expresión lickety-split, que en inglés quiere decir a toda velocidad. Y empieza como siempre: el Coyote con su letrero en latín inventado, Apetitius Giganticus, y el Correcaminos pasando como un rayo."),
 dict(src=["LS@80-376", "LS@120-376"], label="LICKETY-SPLAT", cap="ESQUÍS CON RUEDAS",
      txt="Esta vez el Coyote voltea los letreros, y ahora el Correcaminos se llama Fastius Tasty-us, rápido y sabroso. Cuando el Correcaminos acelera, la velocidad enrolla la carretera, voltea un túnel al revés y aplasta un puente. Así que el Coyote prueba con unos esquís con ruedas, y baja por la montaña a toda velocidad. El Correcaminos da una vuelta en U al final de un precipicio. El Coyote, no."),
 dict(src=["LS@180-376", "LS@210-376"], label="LICKETY-SPLAT", cap="EL GLOBO",
      txt="Después viene un arco y flecha, que termina con el Coyote atorado de cabeza en la orilla de un barranco. Y luego un globo aerostático, cargado de bombas con forma de dardo. Ya te imaginas cómo termina cada intento. Y en esta caricatura también aparece un bumerán, con la etiqueta regresa a su dueño, que hace exactamente lo que promete."),

 dict(src=["AS@40-356", "AS@60-356"], label="THE ABOMINABLE SNOW RABBIT", cap="#2",
      txt="Número dos: The Abominable Snow Rabbit, el abominable conejo de las nieves. La dirigió Chuck Jones, con Maurice Noble como codirector y una historia de Tedd Pierce. Se estrenó el veinte de mayo de 1961, con Bugs Bunny y el Pato Lucas. Los dos iban cavando un túnel rumbo a Palm Springs, en California, pero por una vuelta equivocada terminan en las montañas del Himalaya."),
 dict(src=["AS@100-356", "AS@160-356"], label="THE ABOMINABLE SNOW RABBIT", cap="HUGO",
      txt="Lucas, furioso, decide regresar a Perth Amboy, pero bajo tierra se encuentra con Hugo, un yeti gigante que lo confunde con un conejo. Y Hugo quiere mucho a sus conejos: los abraza, los aprieta y los aplasta con un cariño que rompe huesos. Lucas, desesperado, le dice que el verdadero conejo es Bugs. Y ahora los dos tienen que escapar del abrazo más peligroso del Himalaya."),
 dict(src=["AS@300-356", "AS@330-356"], label="THE ABOMINABLE SNOW RABBIT", cap="LA ÚLTIMA DE LUCAS",
      txt="Al final, todos terminan en Palm Springs, y el calor del desierto hace lo suyo: Hugo se derrite hasta quedar en un charco. Bugs comenta que, después de todo, era solo un muñeco de nieve. Y Lucas, empapado, responde: abominable, eso es lo que es. Un dato para los fans: esta fue la última caricatura original de cine de Chuck Jones con el Pato Lucas. Y la voz de Bugs, de Lucas y de Hugo era de Mel Blanc."),

 dict(src=["NF@40-440", "NF@60-440"], label="NELLY'S FOLLY", cap="#1",
      txt="Y el número uno: Nelly's Folly, la locura de Nelly, escrita y dirigida por Chuck Jones, con Maurice Noble y Abe Levitow como codirectores. Se estrenó el treinta de diciembre de 1961. Como en One Froggy Evening, la del sapo cantante, la historia es sobre el descubrimiento de un animal que canta. Pero aquí la protagonista es el animal: Nelly, una jirafa que vive en África."),
 dict(src=["NF@100-440", "NF@160-440"], label="NELLY'S FOLLY", cap="DE ÁFRICA A NUEVA YORK",
      txt="Nelly canta tan bonito que todos los animales se detienen a escucharla. Un cazador que pasa por ahí la convence de hacerse profesional, y le ofrece un contrato. Así que Nelly deja la selva y se va a Nueva York. Empieza en comerciales y presentaciones en vivo, y poco a poco se convierte en una cantante exitosa, en una estrella de la moda, con su cara en anuncios por toda la ciudad."),
 dict(src=["NF@290-440", "NF@340-440"], label="NELLY'S FOLLY", cap="LA FAMA",
      txt="Pero la fama la deja sola. Buscando amor, Nelly llega al zoológico, donde un jirafo casado la enamora. El romance se vuelve escándalo, su representante la abandona, y un día su espectáculo se estrena ante un teatro vacío. Nelly termina llorando en un puente, y el narrador dice que sus fans esperan que haya vuelto a casa. Es una caricatura sorprendentemente triste para la época."),
 dict(src=["NF@400-440", "NF@264-440"], label="NELLY'S FOLLY", cap="EL ÓSCAR",
      txt="Pero tiene final feliz: de vuelta en África, Nelly canta una canción triste, y un jirafo la acompaña con su voz. Los dos se enamoran. La voz cantada de Nelly era de Gloria Wood. Y Nelly's Folly fue nominada al Óscar al mejor cortometraje animado de 1962. No ganó: el premio fue para Surogat, un corto de Yugoslavia. Pero hoy es considerada una de las joyas escondidas de Chuck Jones."),

 dict(src=["NF@264-440", "PV@226-376"], label=L, cap="",
      txt="Seis caricaturas de 1961, el año de Kennedy, de Gagarin, de Alan Shepard y del estreno de Don Gato y su pandilla. ¿Cuál de estas recordabas? ¿O hay otra caricatura de 1961 que te marcó de niño? Cuéntanos en los comentarios. Y si te perdiste los años anteriores, en el canal ya tenemos muchas más listas, año por año. Suscríbete, porque la serie sigue."),
]
json.dump(S, open("script.json", "w"), ensure_ascii=False, indent=1)
print(len(S), sum(len(s["txt"].split()) for s in S))
