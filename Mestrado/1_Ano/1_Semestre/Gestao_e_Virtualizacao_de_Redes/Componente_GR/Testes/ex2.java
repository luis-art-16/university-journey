import java.io.*;
import java.util.*;

class Produto {
    String codigo;
    String nome;
    int stock;
    double preco;

    Produto(String c, String n, int s, double p) {
        codigo = c;
        nome = n;
        stock = s;
        preco = p;
    }
}

public class Ex2 {
    public static void main(String[] args) throws Exception {
        if (args.length == 0) {
            System.out.println("java Ex2 <inventario.csv>");
            return;
        }

        String ficheiro = args[0];
        HashMap<String, Produto> map = new HashMap<String, Produto>();

        BufferedReader br = new BufferedReader(new FileReader(ficheiro));
        String linha = br.readLine(); // cabeçalho
        while ((linha = br.readLine()) != null) {
            if (linha.length() == 0) continue;
            String[] campos = linha.split(",");
            String codigo = campos[0];
            String nome = campos[1];
            int stock = Integer.parseInt(campos[2]);
            double preco = Double.parseDouble(campos[3]);
            Produto p = new Produto(codigo, nome, stock, preco);
            map.put(codigo, p);
        }
        br.close();

        BufferedReader stdin = new BufferedReader(new InputStreamReader(System.in));
        String cmdLine;
        while ((cmdLine = stdin.readLine()) != null) {
            if (cmdLine.length() == 0) continue;
            String[] p = cmdLine.split("\\s+");  // p é o array de tokens pedido
            String op = p[0];

            switch (op) {
                case "END":
                    stdin.close();
                    return;

                case "INC": {
                    String codigo = p[1];
                    int qtd = Integer.parseInt(p[2]);
                    Produto prod = map.get(codigo);
                    if (prod == null) {
                        System.out.println("codigo não encontrado");
                    } else {
                        prod.stock = prod.stock + qtd;
                    }
                    break;
                }

                case "DEC": {
                    String codigo = p[1];
                    int qtd = Integer.parseInt(p[2]);
                    Produto prod = map.get(codigo);
                    if (prod == null) {
                        System.out.println("codigo não encontrado");
                    } else if (qtd <= 0) {
                        System.out.println("quantidade incorreta");
                    } else if (prod.stock < qtd) {
                        System.out.println("stock insuficiente");
                    } else {
                        prod.stock = prod.stock - qtd;
                    }
                    break;
                }

                case "LIST": {
                    ArrayList<Produto> lista = new ArrayList<Produto>(map.values());

                    Collections.sort(lista, new Comparator<Produto>() {
                        public int compare(Produto a, Produto b) {
                            return a.nome.compareToIgnoreCase(b.nome);
                        }
                    });

                    int z = 0;
                    while (z < lista.size()) {
                        Produto prod = lista.get(z);
                        System.out.println(prod.codigo + "," + prod.nome + "," +
                                           prod.stock + "," + prod.preco);
                        z = z + 1;
                    }
                    break;
                }

                default:
                    System.out.println("comando inválido");
                    break;
            }
        }
        stdin.close();
    }
}
