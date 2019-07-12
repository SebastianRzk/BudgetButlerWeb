<?php

require_once __DIR__."/dtos/Einzelbuchung.php";
// src/Product.php
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

    public function asDTO() {
	$dto = new EinzelbuchungDTO();
	$dto->id = $this->id;
	$dto->datum = $this->getDatum();
	$dto->name = $this->getName();
	$dto->kategorie = $this->getKategorie();
	$dto->wert = $this->getWert();
	return $dto;
    }
}
