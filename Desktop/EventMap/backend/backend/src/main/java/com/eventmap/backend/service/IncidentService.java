package com.eventmap.backend.service;

import com.eventmap.backend.entity.Incident;
import com.eventmap.backend.repository.IncidentRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class IncidentService {

    private final IncidentRepository incidentRepository;

    public IncidentService(IncidentRepository incidentRepository) {
        this.incidentRepository = incidentRepository;
    }

    public Incident createIncident(Incident incident) {
        return incidentRepository.save(incident);
    }

    public List<Incident> getAllIncidents() {
        return incidentRepository.findAll();
    }

    public Incident getIncidentById(Long id) {
        return incidentRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found"));
    }

    public Incident updateIncident(Long id, Incident updatedIncident) {

        Incident existingIncident = getIncidentById(id);

        existingIncident.setTitle(updatedIncident.getTitle());
        existingIncident.setDescription(updatedIncident.getDescription());
        existingIncident.setSeverity(updatedIncident.getSeverity());
        existingIncident.setStatus(updatedIncident.getStatus());
        existingIncident.setUpdatedAt(updatedIncident.getUpdatedAt());
        existingIncident.setResolvedAt(updatedIncident.getResolvedAt());
        existingIncident.setReportedBy(updatedIncident.getReportedBy());

        return incidentRepository.save(existingIncident);
    }

    public void deleteIncident(Long id) {
        incidentRepository.deleteById(id);
    }
}