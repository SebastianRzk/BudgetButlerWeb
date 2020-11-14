<?php
require_once __DIR__."/dtos/EinzelbuchungDto.php";

/**
 * @Entity @Table(name="einzelbuchungen")
 **/
class Einzelbuchung
{
    /** @Id @Column(type="integer") @GeneratedValue **/
    protected $id;
    /** @Column(type="string") **/
    protected $name;
    /** @Column(type="string") **/
    protected $user;
    /** @Column(type="string") **/
    protected $kategorie;
    /** @Column(type="date") **/
    protected $datum;
    /** @Column(type="decimal") **/
    protected $wert;

    public function getName()
    {
        return $this->name;
    }

    public function getKategorie()
    {
        return $this->kategorie;
    }

    public function getDatum()
    {
        return $this->datum;
    }

    public function getWert()
    {
        return $this->wert;
    }

	public function setName($name) { $this->name = $name;}
	public function setKategorie($kategorie) { $this->kategorie = $kategorie;}
	public function setUser($user) { $this->user = $user;}
	public function setDatum($datum) { $this->datum = $datum;}
	public function setWert($wert) { $this->wert = $wert;}

    public function asDto() {
	$dto = new EinzelbuchungDto();
	$dto->id = $this->id;
	$dto->datum = $this->getDatum()->format('Y-m-d');
	$dto->name = $this->getName();
	$dto->kategorie = $this->getKategorie();
	$dto->wert = $this->getWert();
	return $dto;
    }
}
