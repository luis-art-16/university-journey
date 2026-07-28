                      Teste de Poo (8 valores (1.1 + 1.2) = passei)

1.1 - Completar um classe que é dada logo no inicio do teste e apresentar os seus construtores 
e os vários métodos necessários para satisfazer o enunciado. (4 valores)

O que nos podem dar logo no incio é:

Public abstract class X
{
   private String a;
   private double b;
   private int c;
   private Set<Integer> d;
   private Map<Integer, Integer> e;
   private List<servico> servicos;
   private Map<Integer,List<Integer>> f;
}

...
...

public abstract double g();
public abstract X clone();

Alguns desses métodos podem ser:
   1- Adicionar um nova coisa 
   2- listar qualquer coisa
   3- Adicionar uma coisa a alguém
   4- Obter a totalidade de algo
   5- Obter uma lista relativa a algo ou alguém

Código Base para responder à pergunta:

// Completar a classe dada de acordo com o que nos dão incialmente:

dado no enunciado - Public abstract class X {
   private String a;
   private double b;
   private int c;
   private Set<Integer> d;
   private Map<Integer, Integer> e;
   private List<servico> servicos;
   private Map<Integer,List<Integer>> f;
}

public abstract double g();
public abstract X clone();

//Começamos por definir as variáveis:

public X(String a, double b, int c) {
   this.a = a;
   this.b = b;
   this.c = c;
   this.d = new HashSet<Integer>();
   this.e = new HashMap<Integer, Integer>();
   this.servicos = new ArrayList<Servico>();
   this.f = new HashMap<Integer,List<Integer>>();
}

//Gets 

public String getA() {
   return this.a;
}

public double getB() {
   return this.b;
}

public double getC() {
   return this.c;
}

public Set<Integer> getD() {
   return new HashSet<>(d);
}

//Métodos

 1 - Adicionar uma nova coisa

 public void add(int c, ...) {
  this.f.put(c, new ArrayList<Integer>());
 }

 ou

 public int e_qqcoisa(int c) {
   if(this.e.constainsKey(c))
   return this.e.get(c);
   else  return 0;
}

 public void add(int c, String a) {
   this.e.put(c, this.e_qqcoisa(c)+a);
 }

 2 - listar qualquer coisa

 public List<Integer> getListadeqqcoisa(int c) {
   ArrayList<Integer> novalista = new ArrayList<Integer>();
   if(this.f.constainsKey(c))
   {
      for(int y : this.f.get(c))
      novalista.add(y);
   }
   return novalista;
}

3 - Adicionar uma coisa a alguém

public void nova_coisa(int c, int coisa) {
   if(this.f.constainsKey(c)) {
      this.f.get(c).add(coisa);
   }
}

4- Obter a totalidade de algo

public int total_algo() {
   int total = 0;
   for(int a : this.algo.values()) {
      tot += a; 
   }
      return total;
}  

5- Obter uma lista relativa a algo ou alguém - exemplo para um servico

public void add(Servico s) {
   this.servico = add(s);
   for(Integer c : s.alguem()) {
      this.add(c, s.tempo());
   }
}

public List<Servico> Lista () {
   ArrayList<Servico> lista = new ArrayList<Servico> ();
   for(Servico s : this.servico) {
      lista.add(s);
   }
   return lista;
}

1.2 - Apresentar a implementação das subclasses da Classe X com variáveis de instância,  (4 valores)
construtores e métodos adicionais. Normalmente são 2 classes: Classe Y e Classe Z: 

public class Y extends X {

   public Y(String a, double b, int c) {
   super(a, b, c);                              //variáveis de instância

}

// Construtores dados no enunciado: public abstract double g(); public abstract X clone();

public double g() { 
 double result == 0.0;
 for(int c: super.c()) {
   result +=super.g_c(c);
 }
 return result / super.c().size();
}

public Y clone() {
   Y novo = new;
   Y(super.getA(),super.getB(),super.getC());

   for(int c : super.c()) {
      novo.add(c);
      for(int c2 : super.getA()) {
         novo.nova_coisa(c,c2);
      }
      return novo; 
   }
}

}

public classe Z extends X {
   
   private int var; //variavel de instancia
   public Z(String a, double b, int c, int v) {
      super(a, b, c);
      this.var = v;
   }

   public int getVar() {
      return this.var;
}

   public double g() { 
   double result == 0.0;
   int total = 0;
   
   for(int c : super.c()) {
   total += super.getaA(a).size();
   
   for(int t:super.getA(a)) {
      result += t;
   }
   }
   result = result/(double)total;
}


   public Z clone() {
      Z novo = new;
      Z(super.getA(),super.getB(),super.getC(),this.var);

      for(int c : super.c()) {
         novo.add(c);
         for(int c2 : super.getA()) {
            novo.nova_coisa(c,c2);
      }
         return novo; 
      }
   }
}

1.3 - Implementar uma classe em geral, muito parecida com a implementação das subclasses acima, mas com novas variáveis de instância (1 valor)

2.1 - Implementar uma classe W que representa a classe X (como por exemplo a Universidade representar as turmas que nela existem) que contém especificos parametros
associados à classe X e permite adicionar um X (turma, patrulha, hotel,etc). Não esquecer claro das var de instancia, construtores e métodos adicionais.


public class W {
   //variaveis de instancia
   private HashMap<Integer,X> lista;
   private Map<Integer,List<Integer>> clientes;

   //construtor
   public W() {
      this.lista = new HasMap<Integer,X>();
      this.clientes = new HashMap<Integer,List<Integer>>();
   } 
      public void add (X p) {
      if(p != null) {
         this.lista.put(p.getA(), p.clone());
         }
      }

      // em caso do exercicio pedir para lançar uma execeção basta mudar o seguinte:
      public void add (X p) throws JaExisteException {
         if(this.lista.containsKey(p.getA())) {
            throw new JaExisteException ("Isto já existe")
            }
         else {
            this.lista.put(p.getA(), p.clone());
            }
            
         }
   }
   
2.2 - Escrever um método, geralmente é public int maior_custo que identifica alguma coisa associada a esse custo.
Caso mude o nome do método, apenas altera a lógica associada ao este, mas mantém a estrutura. (2 valores)

    public int maior_custo() {
    
      double max = 0.0;
      int variable = 0;
      for(X p : this.lista.values()) {
         if(p.custo() > max) {
            max = p.custo();
            variable = p.getA();
            }
      }
}

2.3 - Escrever um método public Set<X> ordemX() que identifica / retorna um conjunto ordenado ascendente/descendente 
de acordo com um termo especifico associado a X (3 valores)

public Set<X> ordemX() {
   //ordem ascendente (caso peça descendende é só trocar os membros a e b)

   TreeSet<X> nova = new TreeSet<X>((a,b) -> (int)(a.media() - b.media()))
   for(X p : this.lista.values()) {
      nova.add(p.clone());
      }
     return nova;
}

Nota: Em caso de não ter tempo, melhor optar por fazer a 2.3 do que a 2.4

2.4 - Escrever um método que identifique algo relacionado com a classe X de forma a obter a sua majoridade (3 valores)

public int algomaisX() { // nome do método é dado no enunciado 

 HashMap<Integer,Integer> m = new HashMap<Integer,Integer>();

 for(X p : this.lista.values()) {
   if(m.containsKey(p.getA())) {
      m.put(p.getA(), m.get(p.getA())+1);
   }
else {
   m.put(p.getA(), 1);
   }
}

int max = 0;
int a = 0;
for(int x : m.keySet()) {
   if(m.get(x)> max) {
      max = m.get(x);
      a = x;
      }
   }
      return a;
}
 
2.5 - Escrever um método que identifica "tempo" relacionado com termos associados à classe X. Assumindo um certo "tempo" dado no enunciado. (2 valores esta é pó 20 rsrsrs)

public String tempo() {

   HashMap<Integer, Integer> m2 = new HashMap<Integer, Integer>();
   for(X p : this.lista.values()) {
      if(m.containsKey(p.getA())) {
      m.put(p.getA(), m.get(p.getA()));
      m2.put(p.getA(),m2.get(p.getA())+1);
      }
      else {
         m.put(p.getA());
         m2.put(p.getA(),1);
      }
}
// Provavelmente é necessário adicionar outras lógicas 

Iterator<Integer> i = m.keySet().iterator();
While (i.hasNext()) {
total = 0;
int max = 0;
int r = i.next();
if(m.get(r).equals)
{
   total ++;
   incio = r;
   int fim = r;
}
   boolean flag = true;
   While(i.hasNext()&&flag){
      r = i.next();
      if(m.get(r).equals) {
         total ++;
         fim = r;
      }
      else 
      flag = false;
   }
   if(total > max) {
      max = total;
      }  
   }
}


