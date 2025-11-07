from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class Usuario(models.Model):
    """
    Modelo para a tabela 'usuário'.
    """
    # Opções para o campo 'cargo'
    class Cargo(models.TextChoices):
        COORDENADOR = 'Coordenador', 'Coordenador'
        SUPERVISOR = 'Supervisor', 'Supervisor'
        SECRETARIA = 'Secretaria', 'Secretaria'
        ESTAGIARIO = 'Estagiario', 'Estagiario'
        RESPONSAVEL_TEC = 'ResponsavelTec', 'ResponsavelTec'

    # O SQL especificava 'iduser SERIAL PRIMARY KEY'.
    # AutoField do Django é o equivalente a SERIAL.
    iduser = models.AutoField(primary_key=True)
    
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    
    # EmailField faz uma validação básica de email
    emailinst = models.EmailField(max_length=150, unique=True, null=False, blank=False)
    
    cpf = models.CharField(max_length=30, unique=True, null=False, blank=False)
    matricula = models.CharField(max_length=15, unique=True, null=False, blank=False)
    
    # !! AVISO DE SEGURANÇA !!
    # Nunca armazene senhas como CharField.
    # O sistema de autenticação do Django (Auth) deve ser usado
    # para armazenar senhas de forma segura (com hash).
    # Este campo está aqui apenas para refletir o SQL.
    senha = models.CharField(max_length=255, null=False, blank=False)
    
    # auto_now_add=True é o equivalente a 'DEFAULT NOW()' na criação
    dthinsert = models.DateTimeField(auto_now_add=True)
    
    # Usando 'choices' para implementar a restrição CHECK do SQL
    cargo = models.CharField(
        max_length=25,
        choices=Cargo.choices,
        null=False,
        blank=False
    )
    
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'usuário'  # Força o nome da tabela a ser exatamente 'usuário'

    def __str__(self):
        return f"{self.name} ({self.cargo})"


# NOTA SOBRE FOTOS (bytea / BinaryField):
# Armazenar arquivos/imagens no banco de dados (como bytea/BinaryField)
# geralmente não é recomendado por questões de performance.
# A prática comum no Django é usar 'ImageField', que salva o arquivo
# no sistema de arquivos (ou num serviço de storage como S3)
# e armazena apenas o *caminho* para o arquivo no banco de dados.

class Coordenador(models.Model):
    """
    Modelo para a tabela 'coordenador'.
    O campo 'crp' é usado como Primary Key para as Foreign Keys.
    """
    crp = models.IntegerField(primary_key=True, verbose_name="CRP")
    
    # Relacionamento auto-referenciado (um coordenador pode ser subordinado a outro)
    # 'self' refere-se à própria classe (Coordenador)
    crpcoord = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,  # Se o coordenador "pai" for deletado, seta este campo para NULL
        null=True,
        blank=True,
        db_column='crpcoord',
        related_name='subordinados'
    )
    
    dthcoord = models.DateTimeField(auto_now_add=True)
    
    # Equivalente a 'bytea'. Veja a nota sobre ImageField acima.
    foto_cooder = models.BinaryField(null=True, blank=True)
    
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'coordenador'
        verbose_name = "Coordenador"
        verbose_name_plural = "Coordenadores"

    def __str__(self):
        return f"Coordenador CRP: {self.crp}"


class Supervisor(models.Model):
    """
    Modelo para a tabela 'supervisor'.
    O campo 'crp' é usado como Primary Key para as Foreign Keys.
    """
    # FK para Coordenador
    crpcoord = models.ForeignKey(
        Coordenador,
        on_delete=models.PROTECT,  # Impede a exclusão de um Coordenador se houver Supervisores ligados a ele
        null=False,
        db_column='crpcoord',
        related_name='supervisores'
    )
    
    crp = models.IntegerField(primary_key=True, verbose_name="CRP")
    
    foto_coord = models.BinaryField(null=True, blank=True)
    dthsup = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'supervisor'
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"

    def __str__(self):
        return f"Supervisor CRP: {self.crp}"


class Secretaria(models.Model):
    """
    Modelo para a tabela 'secretaria'.
    O SQL não especificou uma Primary Key, então o Django
    adicionará um campo 'id' automaticamente (AutoField).
    O campo 'matricula_fun' foi mantido como um Integer.
    """
    crpcoord = models.ForeignKey(
        Coordenador,
        on_delete=models.PROTECT,
        null=False,
        db_column='crpcoord',
        related_name='secretarias'
    )
    
    dthsec = models.DateTimeField(auto_now_add=True)
    
    # O SQL não definiu como 'UNIQUE', então mantivemos assim.
    # Se 'matricula_fun' DEVE ser a Primary Key, mude para:
    # matricula_fun = models.IntegerField(primary_key=True)
    matricula_fun = models.IntegerField(null=False)
    
    foto_sec = models.BinaryField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'secretaria'
        verbose_name = "Secretaria"
        verbose_name_plural = "Secretarias"

    def __str__(self):
        # Se matricula_fun não for única, talvez seja melhor usar o self.id
        return f"Secretaria Matrícula: {self.matricula_fun} (ID: {self.id})"


class RespTec(models.Model):
    """
    Modelo para a tabela 'resptec' (Responsável Técnico).
    O campo 'crpresp' é usado como Primary Key.
    """
    crpcoord = models.ForeignKey(
        Coordenador,
        on_delete=models.PROTECT,
        null=False,
        db_column='crpcoord',
        related_name='responsaveis_tecnicos'
    )
    
    crpresp = models.IntegerField(primary_key=True, verbose_name="CRP Responsável")
    dthresp = models.DateTimeField(auto_now_add=True)
    foto_resptec = models.BinaryField(null=True, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'resptec'
        verbose_name = "Responsável Técnico"
        verbose_name_plural = "Responsáveis Técnicos"

    def __str__(self):
        return f"Resp. Técnico CRP: {self.crpresp}"


class Estagiario(models.Model):
    """
    Modelo para a tabela 'estagiario'.
    O campo 'ra' (Registro Acadêmico) é usado como Primary Key.
    """
    crpsup = models.ForeignKey(
        Supervisor,
        on_delete=models.PROTECT,
        null=False,
        db_column='crpsup',
        related_name='estagiarios'
    )
    
    crpcoord = models.ForeignKey(
        Coordenador,
        on_delete=models.PROTECT,
        null=False,
        db_column='crpcoord',
        related_name='estagiarios'
    )
    
    ra = models.IntegerField(primary_key=True, verbose_name="RA")
    
    nivelestagio = models.CharField(max_length=10, null=False, blank=False)
    semestre = models.CharField(max_length=10, null=False, blank=False)
    foto_estg = models.BinaryField(null=True, blank=True)
    dthestg = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'estagiario'
        verbose_name = "Estagiário"
        verbose_name_plural = "Estagiários"

    def __str__(self):
        return f"Estagiário RA: {self.ra}"