# Aina Hack - Equip 17: Cerquem el teu nou col·laborador científic

Hauria la tecnologia, finançada amb fons públics,
de quedar-se al laboratori? En resposta a la idea d'una administració al servei del valor de la
transformació digital, plantejem un programari basat en IA que agilitzi i alleugeri els tràmits
requerits per executar un projecte de transferència tecnologica. Així, proposem un sistema
capaç d'identificar solucions en linies de recerca catalanes per a empreses que orbitin
programes com ACCIÓ o Digital Innovation Hub; on sovint es perden oportunitats davant un
aclaparador número de convocatories, propostes i possibles solucions. Fem servir models
codificadors multi-llenguatge per relacionar empreses catalanes amb articles en anglés, i
omplim els camps necessàris de les convocatories aportant el context adient amb una
arquitectura de RAG + Salamandra.

<img width="1444" alt="image" src="https://github.com/user-attachments/assets/b116a7cb-4fe7-498a-a41f-df0f6971f15d">

## Arquitectura

El sistema està construit sobre diversos models del projecte [Aina](https://huggingface.co/projecte-aina).

El sistema està muntat fent servir una màquina de còmput que implementa dos servidors en ports separats. Per una banda, una API que ens dóna accés als models d'inferència i per l'altra el servidor que manega les sol·licituds dels usuaris.
